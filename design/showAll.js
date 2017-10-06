function showAll(layers)
{
    for( var i=0; i<layers.length; i++)
    {
        layers[i].visible = true;
        showAll(layers[i].layers);
    }
}
showAll(app.activeDocument.layers);
