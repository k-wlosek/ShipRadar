# ShipRadar

Application for plotting ships' paths using CSV file with data.

## Usage
#### As a native app
1. Download the latest release from [here](https://github.com/k-wlosek/ShipRadar/releases).
2. Unpack the archive.
3. Run the ShipRadar binary.

#### As a Python script
1. Clone the repository.
2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the script:
    ```bash
    python3 main.py
    ```
4. App will run as a web app on `http://localhost:5025/`.



### Screenshots
Main Window:
![MainWindow.png](media/MainWindow.png)
Filter types:
![Filters1.png](media/Filters1.png)
![Filters2.png](media/Filters2.png)
Selected filter:
![SelectedFilter.png](media/SelectedFilter.png)
Resulting plot:
![Plot.png](media/Plot.png)

### CSV file format
The CSV file should contain the following columns:

LRIMOShipNo, ShipName, ShipType, MovementDateTime, Longitude, Latitude, MoveStatus, Heading, Draught, Speed, Destination, ETA

#### Known issues
- Web app functionality is broken, use the native app instead.
