<h1>LIRYCS VISUALISATION</h1>
<i>driven by Python 3.7 and cairo library</i><br><br>

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


