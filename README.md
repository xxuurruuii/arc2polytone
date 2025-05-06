# arc2polytone
a python script to write polytone-styled arcaea fanmade chart in arccreate

## how to use
- make a chart in arcaea (default: 2.aff) with only singlearctaps and arcs
- copy the SceneControl folder to your chart's path
- run main.py and generate a new chart (default: 3.aff)
- open the chart with arccreate

## how does 2.aff work
- suggested input area: -0.5 <= x <= 1.5, 0.0 <= y <= 1.0
- a single arctap -> a note
- the length of the trace -> rotation angle (360, clockwise, 0=up)
- arc -> slide
- trace with a start same as an arc's start/end -> rotation indicator
- snap colors are automatically generated
- red arctap indicates flick
- check main.py for more information
