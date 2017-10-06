Adobe Illustrator has been used to design the panels.

The main file is [missionBoard.ai](../design/missionBoard.ai).

## layers

Each panel (or components) are composed of three specific layers (defined by their name):
- `front` for every drawing of the buttons, leds, etc.
- `label` for everything that must be printed on the on the wood panels
- `back` for the back side of the panels (dimensions, holes, component's footprint)

When I want to see how the board will look like, I just hide the `back` layers, and display the `front` and `label` layers.
To print the labels, only the `label` layers are shown. To print the backside, only the `back` layers are shown.


## scripts
To hide/show the different layers, I have wrote four small javascript scripts for Illustrator.
- [hideBack.js](../design/hideBack.js) to hide all the `back` layers
- [showAll.js](../design/showAll.js) to show all the layers
- [showBack.js](../design/showBack.js) to show all the `back` layers and hide the others
- [showLabel.js](../design/showLabel.js) to show all the `label` layers and hide the others

These scripts may be loaded with File->Script->Other scripts..., or directly by installing them in `<Illustrator folder>/Presets.localized/en_US/Scripts/` (it may change depending on your OS and illustrator version. Google will help you for that).
