function hideBack(layers)
{
    /* iter over all the layers */
    for(var i=0; i<layers.length; i++)
    {
        var layer = layers[i];
        if (layer.name == "back")
        {
                layer.visible = false;
        }
        else
        {
            hideBack(layer.layers);
        }
    }
}


hideBack(app.activeDocument.layers)
