function showLabel(layers)
{
    /* iter over all the layers */
    for(var i=0; i<layers.length; i++)
    {
        var layer = layers[i];
        if (layer.name == "back")
        {
                layer.visible = false;
        }
        else if (layer.name == "front")
        {
            layer.visible = false;
        }
        else if (layer.name == "label")
        {
            layer.visible = true;
        }
        else
        {
            showLabel(layer.layers);
        }
    }
}


showLabel(app.activeDocument.layers)
