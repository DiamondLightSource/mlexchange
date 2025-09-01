def generate_volseg_settings(task):
    """
    Generates the VolSeg settings file for 2D model training.
    """
    import os
    from jinja2 import Template
    if task == 'train':
        # Load the train template
        with open("/volseg-settings/2d_model_train_settings_template.yaml") as f:
            template = Template(f.read())

        # Render the template with specific train settings
        rendered = template.render(
            training_axes="All",  
            model={
                'type': 'U_net',
                'encoder_name': 'tu-convnextv2_base',
                'encoder_weights': 'imagenet',     
                    }
        )

        with open("/volseg-settings/2d_model_train_settings.yaml", "w") as f:
            f.write(rendered)
        print("Generated 2d_model_train_settings.yaml") 

    elif task == 'predict':
        # Load the predict template
        with open("/volseg-settings/2d_model_predict_settings_template.yaml") as f:
            template = Template(f.read())
    
        # Render the template with specific predict settings
        rendered = template.render(
            quality="medium"
        )

        # Write the rendered settings to a file
        with open("/volseg-settings/2d_model_predict_settings.yaml", "w") as f:
            f.write(rendered)
        print("Generated 2d_model_predict_settings.yaml")  

if __name__ == "__main__":
    # This block is for testing the function directly
    generate_volseg_settings("train")
    print("VolSeg train settings file generated successfully.")