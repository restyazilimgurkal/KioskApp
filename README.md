# Simple Streamlit Kiosk App

This repository contains a simple and versatile Streamlit application designed for use on kiosks. The application features easy navigation with a grid of buttons and a barcode input system for data tracking.

## Features

- **Dynamic Grid of Buttons:** This application displays a grid of buttons that are customizable via a configuration file. You can specify the number of columns for the button grid, as well as the colors, backgrounds, and labels for each button.

- **Barcode Input System:** When a button is clicked, it leads to a page where you can enter barcode information. The data is associated with the selected button and stored in a record.

- **Customizable Appearance:** Most aspects of the application's appearance are customizable via the configuration file, including the logo, page title, and button styles.

## Setup & Installation

1. Clone this repository:

```
git clone https://github.com/yourusername/streamlit-kiosk-app.git
```

2. Navigate to the repository folder:

```
cd streamlit-kiosk-app
```

3. Install the required Python packages:

```
pip install -r requirements.txt
```

4. Run the Streamlit app:

```
streamlit run app.py
```

## Configuration

The application reads its configuration from a `config.ini` file. The general structure of this file is as follows:

```
[General]
title = Your App Title
logo = path/to/logo.png
columns = 3
...

[Button1]
label = Button 1 Label
color = #FFFFFF
background = #000000
font_size = 14px
...

[ButtonN]
...
```

Each `[ButtonN]` section specifies the properties of a button in the grid. The `label` is the text displayed on the button, `color` is the text color, `background` is the background color, and `font_size` is the size of the button text.

The `[General]` section specifies the general properties of the app, such as the app title, the logo file path, and the number of columns in the button grid.

## Usage

After launching the Streamlit app, you will see a grid of buttons according to your configuration. Clicking on any button will bring you to a new page where you can input barcode data. The data is associated with the button you clicked and is stored in a record. You can view all records associated with the current button on the same page.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
