document.body.style.backgroundColor = '#444444';

// let sensorData = {'droneSensors': [[37, 60, 87, 100], [39, 67, 81, 40], [47, 50, 97, 109]]};

let sensorNames = ['Temperature', 'Humidity', 'AQI', 'Altitude'];
let charts = [];

for (let i = 0; i < sensorData['droneSensors'][0].length; i++) {
    let container = document.createElement("div");
    container.classList.add("sensor-container");

    // Create a canvas for the chart
    let chartCanvas = document.createElement("canvas");
    chartCanvas.id = "myChart" + i;
    container.appendChild(chartCanvas);

    // Create a div for the history data
    let historyDiv = document.createElement("div");
    historyDiv.classList.add("history");
    historyDiv.id = "historyDiv" + i;

    let historyText = "<h4>" + sensorNames[i] + " History</h4>";

    for (let j = 0; j < sensorData['droneSensors'].length; j++) {
        historyText += "<p style=\"line-height:10px;\">Reading " + (j + 1) + ": " + sensorData['droneSensors'][j][i] + "</p>";
    }

    historyDiv.innerHTML = historyText;
    container.appendChild(historyDiv);

    document.body.appendChild(container);

    let labels = ["1", "2", "3", "4", "5"];
    let values = sensorData['droneSensors'].map(entry => entry[i]);

    let chart = new Chart(chartCanvas, {
        type: 'line',  // Change type to 'line'
        data: {
            labels: labels,
            datasets: [{
                label: sensorNames[i],
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                pointRadius: 5, // Optional: Increase point size for better visibility
                pointHoverRadius: 8, // Optional: Increase hover point size
                pointBackgroundColor: 'rgba(75, 192, 192, 1)' // Optional: Color of points
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    charts.push(chart)
}


function updateData() {
    fetch('/get_data')  // Assuming you have a route for fetching data
        .then(response => response.json())
        .then(data => {
            sensorData = data['sensorData'];
            // console.log(sensorData)
            for (let i = 0; i < sensorData['droneSensors'][0].length; i++) {
                let values = sensorData['droneSensors'].map(entry => entry[i]);
                charts[i].data.datasets[0].data = values;
                charts[i].update();

                // Update history text
                let historyDiv = document.getElementById("historyDiv" + i);
                let historyText = "<h4>" + sensorNames[i] + " History</h4>";

                for (let j = 0; j < sensorData['droneSensors'].length; j++) {
                    historyText += "<p style=\"line-height:10px;\">Reading " + (j + 1) + ": " + sensorData['droneSensors'][j][i] + "</p>";
                }

                historyDiv.innerHTML = historyText;
            }
        });
}

setInterval(updateData, 10); 