<h1>LIRYCS VISUALISATION</h1>
<i>driven by Python 3.7 and cairo library</i><br><br>

The initial concept is to use Adobe InDesign/Illustrator templates as procedural guidelines for generating visualisations out of given data.<br>

![alt text](https://github.com/vkuchinov/MarkovChainVisualisation/blob/master/layouts/preview.jpg?raw=true "Layouts")<br>

Cyan blocks are placeholder for every piece (line), which is based on 'assets/layout.svg'

![alt text](https://github.com/vkuchinov/MarkovChainVisualisation/blob/master/layouts/preview2.png?raw=true "Layouts")<br>

Basically, this SVG do two things—describes positions for purely procedural elements like line chart and typograpy, and, clones SVG object (paths, circles and etc.) by using their tags and ID attribute. So, if there is a two-coins HMM under certain
block, the code selects <g> <i>(group)</i> with ID 'two', set its position <i>translate(x, y)</i>, filters links and sets category <i>(i.e. storytelling) colours.<br>
