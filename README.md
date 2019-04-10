<h1>LIRYCS VISUALISATION</h1>
<i>driven by Python 3.7 and cairo library</i><br><br>

TODO LIST:
<br>
[-] Generate path instead line segments for line chart<br>
[-] Use block template as well as 8 x group block (fill: none, bold stroke)<br>
[-] Add svg2pdf library to export everything directly to portable format<br>
<br>
[-] planned, [x] done, [!] see comments
<br>
The initial concept is to use Adobe InDesign/Illustrator templates as procedural guidelines for generating visualisations out of given data.<br>

![alt text](https://github.com/vkuchinov/MarkovChainVisualisation/blob/master/layouts/preview.jpg?raw=true "Layouts")<br>

Cyan blocks are placeholder for every piece (line), which is based on 'assets/layout.svg'

![alt text](https://github.com/vkuchinov/MarkovChainVisualisation/blob/master/layouts/preview2.png?raw=true "Layouts")<br>

Basically, this SVG do two things—describes positions for purely procedural elements like line chart and typograpy, and, clones SVG object (paths, circles and etc.) by using their tags and ID attribute. So, if there is a two-coins HMM under certain
block, the code selects <g> <i>(group)</i> with ID 'two', set its position <i>translate(x, y)</i>, filters links and sets category <i>(i.e. storytelling) colours.<br>
  
Each line has 2 CSV files: transcript and pitch:<br><br>

<h3>transcript</h3><br>

```
"startTime","endTime","word","energy"
0,0.31875,"one",78.1514739990234
0.31875,0.64375,"voice",81.07177734375
0.64375,0.875,"can",69.5531387329102
0.875,1.18125,"change",74.3520355224609
1.18125,1.3125,"a",72.6160354614258
1.3125,1.5,"room",70.2819900512695
```
<br>
<h3>pitch</h3><br>

```
"time","pitch"
0,NA
0.0125,186.830230712891
0.025,197.354217529297
0.0375,214.999816894531
0.05,233.349884033203
0.0625,241.460952758789
0.075,246.221054077148
0.0875,259.161376953125
0.1,268.365783691406
0.1125,273.382934570312
0.125,278.196868896484
...
```
<br>
Still, I don't have any ideas how to get HMMs and block colours out of that.<br>
<b>energy</b> stands for word size, <b>pitch</b> is linear scale through time.<br>

<h3>I bet, your visual reference with these two samples are generated, so if you want to have these calculations on my side, you can simply send me your code. Otherwise, I need another col in {name_pitch}, called <b>color with 0-2 range</b>, defining block colours and another file, let's say with <b>hmm</b> suffix, containing something like this:</h3>

```
"time","nodes","links"
0.05,"1","0"
0.21,"0,2","0_1"
0.33,"1","0"
0.40,"1,0","1_0"
0.49,"0","0"
0.57,"1","0"
0.65,"2","0"
0.72,"1,0,2","0_1,1_2"
0.89,"2,0","0,1"
1.01,"1","0"
1.12,"1","0"
1.20,"2","0"
1.28,"0,1","1_0"
1.35,"0,2,1","1_0,2_1,0"
```

where time is x position, nodes values are actually colours and links—0 for self-closing, 1_0 link from node #1 to node #0,
so, for example, for storytelling nodes: 2,0, links: 1-0 means that first node is white, second is dark red, and there is only one link which goes from second node to first one.<br>

The current version could be consiidered as pre-release version. Pretty sure that you want multiple pages PDF's as deliverables. For this purpose, I need much more data, not just for two lines, at lease 6-9.
