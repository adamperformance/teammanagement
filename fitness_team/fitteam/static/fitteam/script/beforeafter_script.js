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
        let direction = document.getElementsByName("direction")
        let before_picture = before[0]
        let after_picture = after[0]
        let before_dir = direction[0]
        let after_dir = direction[1]

        // get the images elements on the page
        const before_picture_img = document.getElementById('before_picture')
        const after_picture_img = document.getElementById('after_picture')

        // set the default value to the default value of the dropdown selector
        // this way pics will show up when the page is loaded
        
        bef_tmp = pics[before_picture.value]
        aft_tmp = pics[after_picture.value]

        before_picture_img.src = bef_tmp[before_dir.value.toLowerCase()]
        after_picture_img.src = aft_tmp[after_dir.value.toLowerCase()]

        // if a before date is selected
        before_picture.addEventListener('change', () => {
            set_pic(before_picture, before_dir, before_picture_img)
        })
    
        // if an after date is selected
        after_picture.addEventListener('change', () => {
            set_pic(after_picture, after_dir, after_picture_img)     
        })

        // if before direction is changed
        before_dir.addEventListener('change', () => {
            set_pic(before_picture, before_dir, before_picture_img)
        })

        // if after direction is changed
        after_dir.addEventListener('change', () => {
            set_pic(after_picture, after_dir, after_picture_img)
        } )


        // functionality: select before and after pics by clicking on pictures displayed
        // !!! additional function needed - when upper selection is changed, delete the below selection!!!

        // create before-after "touples" - one for the actual URLs(selection), one for the elements selected (clicked)
        let click_selection = {"before":"", "after":""}
        let clicked_elements = {"before":"", "after":""}

        document.addEventListener('click', event => {
            
            elem = event.target

            // if nothing is selected yet OR both a before and after is selected and we want a new selection
            if ((click_selection["before"] === "" && elem.nodeName == "IMG") || (click_selection["before"] != "" && click_selection["after"] != "" && elem.nodeName === "IMG")) {
                
                // if both selected, set everything back to "zero"
                if (click_selection["before"] != "" && click_selection["after"] != "" && elem.nodeName === "IMG") {
                    click_selection["before"] = ""
                    click_selection["after"] = ""
                    clicked_elements["before"].style.border = "none"
                    clicked_elements["after"].style.border = "none"
                }


                clicked_elements["before"] = elem
                click_selection["before"] = elem.src
                elem.style.border = "solid"
                elem.style.borderColor = "green"

                // set big before image displayed
                before_picture_img.src = click_selection["before"]
            }

            // if the before is already selected
            else if (click_selection["before"] != "" && click_selection["after"] === "" && elem.nodeName === "IMG") {
                clicked_elements["after"] = elem
                click_selection["after"] = elem.src
                elem.style.border = "solid"
                elem.style.borderColor = "red"

                // set the big after image displayed
                after_picture_img.src = click_selection["after"]
            }
        })
    })
})

function set_pic(picture, direction, picture_img) {

    x = document.getElementsByTagName('img')
    
    for (let i = 0; i < x.length; i++) {
        if (x[i].style.border != "") {
            x[i].style.border = ""
        }
    }

    // get the selected value
    picture_value = picture.options[picture.selectedIndex].value;
    direction_value = direction.options[direction.selectedIndex].value;
    direction_value = direction_value.toLowerCase()

    let chosen_pic_url;

    // loop through the dates
    for (let i = 0; i < dates.length; i++) {

        // if the chosen date matches a date in the list of dates
        if (dates[i] === picture_value) {

            // get the related picture triplet
            chosen_pic_set = pics[dates[i]]
                
            // get the selected picture based on the direction
            chosen_pic_url = chosen_pic_set[direction_value]
        }
    }

    // change the picture url to the selected picture's url
    picture_img.src = chosen_pic_url
}