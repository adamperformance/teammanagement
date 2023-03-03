document.addEventListener('DOMContentLoaded', () => {

    // get json data from backend (format is date:picture url)
    fetch('//127.0.0.1:8000/picture')
    .then(response => response.json())
    .then(data => {
        
        pics = data
        
        console.log(pics)

        // create a list of dates
        dates = Object.keys(pics)

        console.log(dates)
    
        // get the 2 dropdown selectors by name
        let before = document.getElementsByName("before")
        let after = document.getElementsByName("after")
        let before_picture = before[0]
        let after_picture = after[0]

        // get the images elements on the page
        const before_picture_img = document.getElementById('before_picture')
        const after_picture_img = document.getElementById('after_picture')

        // set the default value to the default value of the dropdown selector
        // this way pics will show up when the page is loaded
        before_picture_img.src = pics[before_picture.value]
        after_picture_img.src = pics[before_picture.value]

        // if a date is selected
        before_picture.addEventListener('change', () => {

            // get the selected value
            before_value = before_picture.options[before_picture.selectedIndex].value;
            
            console.log(before_value)
            let chosen_pic_url;

            // loop through the dates
            for (let i = 0; i < dates.length; i++) {

                // if the chosen date matches a date in the list of dates
                if (dates[i] === before_value) {

                    // get the related picture url
                    chosen_pic_url = pics[dates[i]]
                }
            }

            // change the picture url to the selected picture's url
            before_picture_img.src = chosen_pic_url
        })
    
        // comments are the same as for the "before"
        after_picture.addEventListener('change', () => {
            after_value = after_picture.options[after_picture.selectedIndex].value;

            let chosen_pic_url;

            for (let i = 0; i < dates.length; i++) {
                if (dates[i] === after_value) {
                    chosen_pic_url = pics[dates[i]]
                }
            }

            after_picture_img.src = chosen_pic_url        
        })

        

        // functionality: select before and after pics by clicking on pictures displayed
        // maybe add green selection (border) to clicked pictures?

        let click_selection = {"before":"", "after":""}

        document.addEventListener('click', event => {
            console.log(event.target.nodeName)

            elem = event.target

            if (click_selection["before"] === "" && elem.nodeName == "IMG") {
                console.log(elem.src)
                click_selection["before"] = elem.src
                console.log(click_selection)
            }

            if (click_selection["before"] != "" && click_selection["after"] === "" && elem.nodeName == "IMG") {
                console.log(elem.src)
                click_selection["after"] = elem.src
                console.log(click_selection)
            }



        })


    })
})