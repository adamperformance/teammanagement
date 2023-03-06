document.addEventListener('DOMContentLoaded', () => {

    // hide the rows by setting the display property?

    // get json data from backend (format is date:picture url)
    fetch('//127.0.0.1:8000/bw_api')
    .then(response => response.json())
    .then(data => {
        
        bws = data

        dates = []
        day_dates = []
        weights = []
        bfs = []

    
        for (let i = 0; i < bws.length; i++) {
            x = bws[i]
            dates.push(x["date"])
            y = x["date"].split(",")
            day_dates.push(String((y[0])))
            weights.push(x["bodyweight"])
            bfs.push(x["bodyfat"])
        }

        

        // the X axis has the date values (wich is good), but not an actual timeline - i.e. 1 day difference and 1 week difference
        // is the same "lenght" --> should change the type of the X axis

        const ctx = document.getElementById('myChart')

        // new Chart(ctx, {
        //     type: 'line',
        //     data: {
        //         // labels: day_dates,
        //         datasets: [{
        //             label: 'Testsúly',
        //             data: [1,2,3,4,5],
        //             borderWidth: 1
        //     }]
        //     },
        //     options: {
        //         scales: {
        //             y: {
        //                 startarzero: false,
        //             },
        //             x: {
        //                 type: 'time',
        //                 time: {
        //                   // Luxon format string
        //                   tooltipFormat: 'DD T'
        //                 },
        //                 title: {
        //                   display: true,
        //                   text: 'Date'
        //                 }
        //             },
        //         },
        //         responsive: true,
        //         maintainAspectRatio: false
        //     }
        // });


        new Chart(ctx, { 
            type: 'line',
            data: weights,
            options: {
              scales: {
                x: {
                  type: 'time',
                  time: {
                    // Luxon format string
                    tooltipFormat: 'DD T'
                  },
                  title: {
                    display: true,
                    text: 'Date'
                  }
                },
                y: {
                  title: {
                    display: true,
                    text: 'value'
                  }
                }
              },
            },
          });
    })

    
})