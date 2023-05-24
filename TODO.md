# Work to do on the project


### src

#### reader
- [x] filter should accept 2 datetimes - start and end - now accepts datetime as from and minutes to calculate timedelta
- [x] other filter options - adapt to final csv
- [x] check csv for proper headers
- [x] fix unit tests

{'LRIMOShipNo': '9566148', 'ShipName': 'WINDSUPPLIER', 'ShipType': 'Passenger', 'MovementDateTime': '2018-07-18 17:59:33.000', 'Latitude': '56.0010017000000030', 'Longitude': '8.1303400000000003', 'MoveStatus': 'Under way using engine', 'Heading': '312', 'Draught': '2,1', 'Speed': '0', 'Destination': 'ESBJERG', 'ETA': '9999-12-31 23:59:59.000'}


#### calculation
- [ ] calculation class with methods for collecting similar entries by name and points interpolation

#### gui
- [x] delete button for already selected filters and text to indicate what is selected
- [ ] improve readability of the gui

#### tests
- [ ] add missing tests for reader

#### logger
- [ ] improve logging

GPT's implementation of collector splitter for calculation.py
```python
data = [{"no": 1, "name": "John"}, {"no": 1, "name": "Alice"}, {"no": 2, "name": "Bob"}, {"no": 2, "name": "Eve"}]

divided_data = []
for item in data:
    no_value = item["no"]
    found = False
    for sublist in divided_data:
        if sublist[0]["no"] == no_value:
            sublist.append(item)
            found = True
            break
    if not found:
        divided_data.append([item])

print(divided_data)
```
https://flet.dev/docs/controls/plotlychart/
https://datascientyst.com/plot-latitude-longitude-pandas-dataframe-python/
perhaps?