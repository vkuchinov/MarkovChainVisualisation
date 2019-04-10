
"""
LYRIC VISUALISATION

copy_page() nultiple pages???

DEPENDENCIES:
Cairo / PyCairo : https://cairographics.org/pycairo/
librsvg: https://en.wikipedia.org/wiki/Librsvg
    
@author Vladimir V KUCHINOV
@email  helloworld@vkuchinov.co.uk

"""

from xml.dom import minidom

#see dependencies list
import cairo
#standard libraries
import json, csv, random

global svg, data, adds, config, w, h

def hexToRgb(hex_):
    
    hex_ = hex_.lstrip('#')
    lv = len(hex_)
    return tuple(int(hex_[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def remap( v_, min0_, max0_, min1_, max1_):

    return float(min1_) + ((float(max1_) - float(min1_)) / (float(max0_) - float(min0_))) * (float(v_) - float(min0_))

def getGroupByN(N_):
    
    groups = svg.getElementsByTagName('g')
    tag = 'one'
    if N_ == 2: 
        tag = 'two'
    elif N_ == 3:
        tag = 'three'

    for g in groups:
        
        if g.getAttribute('id') == tag: 

            return g
        
    return None
        
def filterLinks(index_, tags_):
    
    for tag in tags_:

        if index_ == tag['id']: return True
    
    return False
    
def renderLineChart(ctx_):
    
    count = 0
    for plot in data:
        
        offsetY = h / (len(data)) * count
        if count > 0: offsetY += 5.669 * count
        last = None
                
        for i in range(0, len(data[plot]['pitch']['time'])):
            
            if data[plot]['pitch']['pitch'][i] != 'NA':
                
                lx = remap(float(data[plot]['pitch']['time'][i]), 0, 1.5, config['linechart']['x'], float(config['linechart']['x']) + float(config['linechart']['w']))
                ly = remap(float(data[plot]['pitch']['pitch'][i]), config['linechart']['min'], config['linechart']['max'], float(config['linechart']['y']) + float(config['linechart']['h']), float(config['linechart']['y']))
                ly += offsetY

                if last != None:
                    
                    ctx_.move_to(last['lx'], last['ly'])
                    ctx_.line_to(lx, ly)
                    ctx_.stroke()
                    
                last = {'lx' : lx, 'ly' : ly }
                
            else:
                
                last = None
                
    
        count += 1
        
def renderBlocks(ctx_):
    
    count = 0
    for plot in data:
        
        offsetY = h / (len(data)) * count
        if count > 0: offsetY += 5.669 * count
        step = float(config['blocks']['w']) / len(data[plot]['pitch']['time'])
                
        for i in range(0, len(data[plot]['pitch']['time'])):
            
            bw = step
            bh = float(config['blocks']['h'])
            bx = float(config['blocks']['x']) + step * i
            by = float(config['blocks']['y']) + offsetY

            c = hexToRgb(config['colors'][data[plot]['type']][random.randint(0, 2)])
            ctx_.set_source_rgb(c[0]/255.0, c[1]/255.0, c[2]/255.0)
            ctx_.rectangle(bx, by, bw, bh)
            ctx_.fill()
            
            ctx_.set_source_rgb(0, 0, 0)
            ctx_.rectangle(bx, by, bw, bh)
            ctx_.stroke()
            
        count += 1
        
def renderType(ctx_):
    
    count = 0
    for plot in data:
        
        offsetY = h / (len(data)) * count
        if count > 0: offsetY += 5.669 * count
                
        for i in range(0, len(data[plot]['transcript']['startTime'])):
            
            tx = remap(data[plot]['transcript']['startTime'][i], 0, 1.5, float(config['baseline']['x']), float(config['baseline']['x']) + float(config['baseline']['w']))
            ty = float(config['baseline']['y']) + offsetY
            tsize = remap(data[plot]['transcript']['energy'][i], 75, 100, 48, 80)
            
            ctx_.set_source_rgb(1.0, 1.0, 1.0)
            ctx_.select_font_face(config['font'], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx_.set_font_size(tsize)
            ctx_.move_to(tx, ty)
            ctx_.text_path(data[plot]['transcript']['word'][i])
            ctx_.fill_preserve()
            ctx_.set_source_rgb(0.0, 0.0, 0.0)
            ctx_.set_line_width(1.5)
            ctx_.stroke()
            
        count += 1
        
def renderHMM(ctx_):
    
    out = ''
    count = 0
    
    for plot in data:
        
        chains = []
    
        for i in range(0, len(data[plot]['hmm']['time'])):
         
            nodes = data[plot]['hmm']['nodes'][i].split(',')
            N = len(nodes)
            links = data[plot]['hmm']['links'][i].split(',')
            
            chain = { 'N': N, 't': data[plot]['hmm']['time'][i],'tags' : [] }
            
            for n in range(0, N):
                
                chain['tags'].append({ 'id': 'Node_' + str(n), "color" : config['colors'][data[plot]['type']][int(nodes[n])] })
    
            for l in range(0, len(links)):
     
                if links[l].find("_") == -1:
                    chain['tags'].append({ 'id': 'Link_' + str(links[l]), "color" : '#000000' })
                else:
                    
                    st = links[l].split('_')
                    chain['tags'].append({ 'id': 'Link_' + str(st[0]) + '_' + str(st[1]), "color" : '#000000' })
                     
            chains.append(chain)
        
        offsetY = h / (len(data)) * count
        if count > 0: offsetY += 5.669 * count
        
        for chain in chains:
            
            group = getGroupByN(chain['N'])
            #set entire group Y position
            x = remap(float(chain['t']), 0.0, 1.5, float(config['chains']['x']), float(config['chains']['x']) + float(config['chains']['w']))
            group.setAttribute('transform', 'translate(' + str(x) + ',' + str(offsetY) + ')')

            #transform="rotate(100)"
            if chain['N'] == 1:
                
                    #pass entire content and change colors
                node = group.getElementsByTagName('circle')[0]
                node.setAttribute('fill', chain['tags'][0]['color'])
                index = node.getAttribute('id').replace('Node_', '')
                
                node.setAttribute('stroke', 'none')
                node.setAttribute('stroke-miterlimit', '0')
 
                if str(chain['tags'][int(index)]['color']) == '#FFFFFF':
                
                    node.setAttribute('stroke', '#000000')
                    node.setAttribute('stroke-miterlimit', '10')
                        
                link = group.getElementsByTagName('path')[0]
                link.setAttribute('fill', '#000000')
                     
            else:
  
                nodes = group.getElementsByTagName('circle')
                for node in nodes:
                    
                    index2 = node.getAttribute('id').replace('Node_', '')
                    node.setAttribute('fill', chain['tags'][int(index2)]['color'])

                    node.setAttribute('stroke', 'none')
                    node.setAttribute('stroke-miterlimit', '0')
                    
                    if str(chain['tags'][int(index2)]['color']) == '#FFFFFF':
    
                        node.setAttribute('stroke', '#000000')
                        node.setAttribute('stroke-miterlimit', '10')
                    
                links = group.getElementsByTagName('path')
                for link in links:
                    
                    index = link.getAttribute('id')
                    link.setAttribute('fill', '#000000')
                    if filterLinks(index, chain['tags']) == False:
                        
                        link.setAttribute('fill', 'none')
                        #parent = link.parentNode
                        #parent.removeChild(link) 
                    
                #pass entire content and change colors
            out += group.toxml()
        count += 1
        
    return out

def parseData():

    data = {}

    for obj in config['data']:
        
        data[obj['id']] = {}
        data[obj['id']]['type'] = obj['type']
        
        for file in config['parser']:
            
            data[obj['id']][file['suffix']] = {}
            
            for attr in file['attributes']:
                
                data[obj['id']][file['suffix']][attr] = []
            
            url = 'data/' + obj['id'] + '_' + file['suffix'] + '.csv'
            with open(url, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter = ',')
                next(reader)
                for row in reader:
                    for i in range(0, len(row)):
                        
                        data[obj['id']][file['suffix']][file['attributes'][i]].append(row[i])
                        if file['attributes'][i] == 'pitch' and row[i] != 'NA':
                            
                            config['linechart']['min'] = min(config['linechart']['min'], float(row[i]))
                            config['linechart']['max'] = max(config['linechart']['max'], float(row[i]))

    return data
    
def getElementAttributeByID(type_, id_, attr_):
    
    group = svg.getElementsByTagName(type_)
    
    for obj in group:
        
        if obj.getAttribute('id') == id_:
            
            return obj.getAttribute(attr_)
    
    return None
    
def setVisualElements():
    
    for ph in config['sets']:
        
        if ph['type'] == 'line':
            
            for el in ph['set']:
                
                config[el]['x'] = getElementAttributeByID(ph['type'], el, ph['attributes'][0])
                config[el]['y'] = getElementAttributeByID(ph['type'], el, ph['attributes'][2])
                config[el]['w'] = float(getElementAttributeByID(ph['type'], el, ph['attributes'][1])) - float(getElementAttributeByID(ph['type'], el, ph['attributes'][0]))
               
        elif ph['type'] == 'rect':
            
            for el in ph['set']:
                
                config[el]['x'] = getElementAttributeByID(ph['type'], el, ph['attributes'][0])
                config[el]['y'] = getElementAttributeByID(ph['type'], el, ph['attributes'][1])
                config[el]['w'] = getElementAttributeByID(ph['type'], el, ph['attributes'][2])
                config[el]['h'] = getElementAttributeByID(ph['type'], el, ph['attributes'][3])

with open('config.json') as config_:  
    config = json.load(config_)
    
config['linechart']['min'] = float("-inf")
config['linechart']['min'] = float("inf")

urls = config['data']

svg = minidom.parse(config['in'])
dims = svg.getElementsByTagName('svg')[0].getAttribute('viewBox').split(" ")

w = float(dims[2])
h = float(dims[3]) * len(urls)

setVisualElements()
data = parseData()

with cairo.SVGSurface(config['out'], w, h) as output:
    
    context = cairo.Context(output)
    
    #render linecharts
    renderLineChart(context)
    
    #render typography
    renderType(context)
    
    #render blocks

    renderBlocks(context)

    context.save()


#render HMM chains
adds = renderHMM(context)

src=open("output.svg","r")
oline= src.readlines()
index = len(oline) - 2
oline.insert(index, adds)
src.close()

src=open("output.svg","w")
src.writelines(oline)
src.close()