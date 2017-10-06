function showBack(layers)
{
    /* iter over all the layers */
    for(var i=0; i<layers.length; i++)
    {
        var layer = layers[i];
        if (layer.name == "back")
        {
                layer.visible = true;
        }
        else if (layer.name == "front")
        {
            layer.visible = false;
        }
        else if (layer.name == "label")
        {
            layer.visible = false;
        }
        else
        {
            showBack(layer.layers);
        }
    }
}


showBack(app.activeDocument.layers)
