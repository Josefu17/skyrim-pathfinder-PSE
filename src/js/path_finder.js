document.getElementsByTagName("body")[0].onload = Init;

/** Defines the log levels in the order of severity */
const LEVELS = ['debug', 'info', 'warn', 'error', 'none'];

/**
 * The current log level determines which messages will be printed.
 *
 * @defaultValue 'none'
 * @description
 * Allowed levels are:
 * - 'debug'  - debug and higher severity messages will be printed.
 * - 'info'   - Info and higher severity messages will be printed.
 * - 'warn'   - Warnings and errors will be printed.
 * - 'error'  - Only error messages will be printed.
 * - 'none'   - No log messages are printed.
 */
const LOG_LEVEL = 'none'; // Default value
const TEST = LOG_LEVEL !== 'none'; // LOG_LEVEL == 'none' deactivates test()

function Init() {
    "use strict";
    c_log('debug', '[Path_finder:global](Init)');

    try {
        //delete noscript-tag from page since js is working
        document.getElementById('noscript').remove();
        document.getElementById('script').remove();
    } catch (e) {
        c_log('error', "[Path_finder:global](Init): ", e);
    }

    let path_finder = new Path_finder();

    if (TEST) {
        path_finder.test();
    }
}

/** Custom logging function that controls the output of log messages
 * based on the defined log level.
 *
 * The severity level of the message can be set to 'debug', 'info', 'warn', 'error' and 'none'.
 * @param {'debug'|'info'|'warn'|'error'|'none'} level - The severity level of the log message.
 * @param {string} message - The main message to be logged.
 * @param {string} [extra1] - An optional extra message, defaults to an empty string.
 * @param {string} [extra2] - Another optional extra message, defaults to an empty string.
 * @param {string} [extra3] - Another optional extra message, defaults to an empty string.
 */
function c_log(level, message, extra1, extra2, extra3) {
    "use strict";
    if (!extra1) {
        extra1 = '';
        extra2 = '';
        extra3 = '';
    } else if (!extra2) {
        extra2 = '';
        extra3 = '';
    } else if (!extra3) {
        extra3 = '';
    }

    // If the log level is 'none', do nothing
    if (level === 'none') {
        return;
    }

    /* Checks if the current log level is equal to or more severe than the specified level.
     * If so, it logs the message to the console.
     */
    if (LEVELS.indexOf(level) >= LEVELS.indexOf(LOG_LEVEL)) {
        console[level](message + extra1 + extra2 + extra3); // Call the corresponding console method based on the level
    }
}

/** Checks if the given string is a valid JSON.
 *
 * This function attempts to parse the string. If the parsing is successful, the string is considered valid JSON.
 * If parsing throws an error, the string is considered invalid.
 *
 * @param {string} string - The string to be checked for valid JSON format.
 *
 * @returns {boolean} Returns `true` if the string is valid JSON, otherwise `false`.
 */
function is_valid_json(string) {
    "use strict";
    c_log('debug', '[Path_finder:global](is_valid_json)');

    try {
        JSON.parse(string);
        return true; // if there is no exception, its valid JSON
    } catch (e) {
        return false; // if there is an exception its invalid JSON
    }
}

/** Checks if the given JSON string is formatted (contains newlines and indentation).
 *
 * This function assumes that a properly formatted JSON string will contain newlines (`\n`)
 * and indentation (at least two spaces). It checks if the string includes both of these characteristics.
 *
 * @param {string} jsonString - The JSON string to check for formatting.
 *
 * @returns {boolean} Returns `true` if the JSON string is formatted (contains newlines and indentation),
 *                    and `false` if the string is compact (single-line).
 */
function is_formatted_json(jsonString) {
    "use strict";
    c_log('debug', '[Path_finder:global](is_formatted_json)');

    return jsonString.includes('\n') && jsonString.includes('  ');
}

/** Formats the given JSON string to be more readable.
 *
 * @param {string|object} string - The string or object to be formatted.
 * @returns {string} The formatted JSON string with indentation for readability.
 */
function format_json(string) {
    "use strict";
    c_log('debug', '[Path_finder:global](format_json)');

    if (is_valid_json(string)) {
        if (!is_formatted_json(string)) {
            string = JSON.parse(string);
            string = JSON.stringify(string, null, 2);
        }
    } else {
        string = JSON.stringify(string, null, 2);
    }

    return string;
}

/**
 * A class responsible for the "Path finder" webpage.
 * It handles the following tasks:
 *
 * - Binds methods to events like form submission and input change.
 * - Validates the form to ensure that both start and endpoint are set before enabling the submit button.
 * - Retrieves form data and processes it by forwarding it to a service.
 * - Handles the service response and updates the webpage with the response data.
 */
class Path_finder {

    /** TODO: write
     *
     */

    // global variables
    /** current disabled option of <select> endpoint
     *
     * if set on 0; nothing is disabled
     * @default 0
     * */
    #currently_disabled = 0;

    /** Binds methods to events/actions and
     * contains further configurations for class path_finder.
     */
    constructor() {
        "use strict";
        c_log('debug', '[Path_finder](constructor)');

        try {
            // deactivate reload of webpage
            document.getElementById('path_points_form').setAttribute('onsubmit', 'return false;');

            this.load_cities();

            // check completion of form with every change
            document.getElementById('path_points_form').oninput = this.check_form_completion.bind(this);
            this.check_form_completion();

            // makes sure, the user cannot select the same city as start- and endpoint
            document.getElementById('startpoint').onchange = this.disable_endpoint.bind(this);

            // process form data with a method
            document.getElementById('path_points_submit_button').onclick = this.process_form_data.bind(this);
        } catch (e) {
            c_log('error', '[Path_finder](constructor): ', e);
        }
    }

    /***/
    load_cities() {
        "use strict";
        c_log('debug', '[Path_finder](load_cities)');

        let counter = 0;

        /* As long as fetching from Backend doesn't work; load json map data
         * response structure: map{"cities": [{...}, ...], "connections": [{...}, ...], "mapname": "..." }
         */
        fetch('../../assets/json/skyrim_information.json')
            .then(response => response.json())
            .then(map => {
                const endpoint_list = document.getElementById('endpoint_list');
                const select_startpoint = document.getElementById('startpoint');
                const select_endpoint = document.getElementById('endpoint');
                map.cities.forEach(city => {
                    let list_item = document.createElement('li');
                    list_item.innerText = city.name;
                    endpoint_list.appendChild(list_item);

                    let option = document.createElement('option');
                    option.value = (++counter).toString();
                    option.textContent = city.name;
                    select_startpoint.appendChild(option);

                    option = document.createElement('option');
                    option.value = counter.toString();
                    option.textContent = city.name;
                    select_endpoint.appendChild(option);
                });
            })
            .catch(error => c_log('error', '[Path_finder](load_cities): Error fetching cities:', error));
    }

    /** Disables the city selected as startpoint for the endpoint selection
     */
    disable_endpoint() {
        "use strict";
        c_log('debug', '[Path_finder](disable_endpoint)');

        let to_be_disabled = 0;

        let startpoint = document.getElementById('startpoint');
        for (let child of startpoint.children) {
            if (child.selected) {
                c_log('info', '[retrieve_form_data]: startpoint set to ', child.getAttribute('value'), child.innerText);
                to_be_disabled = parseInt(child.value);
                break;
            }
        }
        let endpoint = document.getElementById('endpoint');

        if (to_be_disabled === 0) {

            endpoint.children.item(this.#currently_disabled).disabled = false;
            endpoint.children.item(0).disabled = false;

        } else if (to_be_disabled !== this.#currently_disabled) {

            endpoint.children.item(this.#currently_disabled).disabled = false;

            if (endpoint.children.item(to_be_disabled).selected) {
                endpoint.children.item(0).selected = true;
            }

            endpoint.children.item(to_be_disabled).disabled = true;
        }

        this.#currently_disabled = to_be_disabled;
        this.check_form_completion();
    }

    /** Method for testing in general.
     *
     * TODO: remove if not needed anymore
     */
    test() {
        "use strict";
        c_log('debug', '[Path_finder](test)');

        // Auto selects start and endpoint to directly enable the submit button for testing
        document.getElementById("startpoint").selectedIndex = 0;
        document.getElementById("endpoint").selectedIndex = 0;
        this.check_form_completion();

        // Test cases with different log levels
        if (LEVELS.indexOf('debug') === LEVELS.indexOf(LOG_LEVEL)) {
            c_log('debug', '[Path_finder](test): This is a debug message'); // Will not show, because LOG_LEVEL is 'warn'
            c_log('info', '[Path_finder](test): This is an info message');  // Will not show, because LOG_LEVEL is 'warn'
            c_log('warn', '[Path_finder](test): This is a warning message'); // Will show, because LOG_LEVEL is 'warn' or higher
            c_log('error', '[Path_finder](test): This is an error message'); // Will always show, because 'error' is the highest level
            c_log('none', '[Path_finder](test): This message should not be logged'); // Will not show, because the level is 'none'
        }
    }

    /** Checks if the form is filled out correctly.
     *
     * If both the start and endpoint are set,
     * the submit button is enabled;
     * otherwise, the button is disabled.
     */
    check_form_completion() {
        "use strict";
        c_log('debug', '[Path_finder](check_form_completion)');

        try {
            let listItems = document.getElementById("path_points_form").childElementCount;
            let startpoint_is_set = !(document.getElementById("startpoint").value === "0" ||
                document.getElementById("startpoint").value === "");
            let endpoint_is_set = !(document.getElementById("endpoint").value === "0" ||
                document.getElementById("startpoint").value === "");
            let button = document.getElementById("path_points_submit_button");
            button.disabled = !(listItems > 1 && startpoint_is_set && endpoint_is_set);
        } catch (e) {
            c_log('error', '[Path_finder](check_form_completion): ', e);
        }
    }

    /** Processes form data by performing the following steps:
     *
     * - Retrieves form data.
     * - Forwards the data to a service.
     * - Awaits the response from the service.
     * - Updates the webpage with the response data.
     *
     * @async Due to Service communication.
     */
    async process_form_data() {
        "use strict";
        c_log('debug', '[Path_finder](process_form_data)');

        let form_data = this.retrieve_form_data();
        c_log('info', '[Path_finder](process_form_data): ', form_data);

        try {
            let response_data = await this.get_route(form_data);

            this.update_response_section(response_data);
        } catch (e) {
            c_log('error', '[Path_finder](process_form_data): ', e);
        }
    }

    /** Retrieves selected values from "startpoint" and "endpoint" form elements.
     *
     * @example
     * Example usage:
     *   let formData = retrieve_form_data();
     *   console.log(formData);
     *   // or
     *   c_log('info', formData);
     * Output:
     *   '{ "startpoint": "Start Location", "endpoint": "End Location" }'
     *
     * @returns {string} A JSON string representing the selected `startpoint` and `endpoint` values.
     */
    retrieve_form_data() {
        "use strict";
        c_log('debug', '[Path_finder](retrieve_form_data)');

        let form_data = {};

        // Retrieve form data
        let startpoint = document.getElementById('startpoint');
        for (let child of startpoint.children) {
            if (child.selected) {
                c_log('info', '[Path_finder](retrieve_form_data): ', child.getAttribute('value'), child.innerText);
                form_data.startpoint = child.innerText;
            }
        }
        let endpoint = document.getElementById('endpoint');
        for (let child of endpoint.children) {
            if (child.selected) {
                c_log('info','[Path_finder](retrieve_form_data): ', child.getAttribute('value'), child.innerText);
                form_data.endpoint = child.innerText;
            }
        }

        return JSON.stringify(form_data, null, 2);
    }

    /** Sends given form data to a remote service using the GET-method and returns its response.
     *
     * @param {string} request_body A JSON string
     *
     * @example
     * request body:
     * {
     *   "startpoint": "<Markarth>",
     *   "endpoint": "<Karthwasten>"
     * }
     * response body:
     * {
     *   "route": {
     *     "0": "Markarth",
     *     "1": "Karthwasten"
     *   },
     *   "distance": 321.1230293828208
     * }
     *
     * @returns {string} A JSON string representing "route" and "distance" for given "startpoint" and "endpoint".
     */
    async get_route(request_body) {
        "use strict";
        c_log('debug', '[Path_finder](get_route)');

        request_body = format_json(request_body);
        c_log('info', '[Path_finder](get_route): ', request_body);

        // As long as fetching in general doesn't work; use the request body itself as response
        let response_data = request_body;

        // As long as fetching from Backend doesn't work; load json map data
        await fetch('../../assets/json/skyrim_information.json', {
            method: 'GET', // Standardmethode ist GET, aber du kannst auch andere Methoden wie POST verwenden
            headers: {
                'Content-Type': 'application/json; charset=utf-8', // Setzt den Content-Type Header
            }
        })
            .then(response => response.json())
            .then(data => {
                response_data = data;
            })
            .catch(error => c_log('error', '[Path_finder](get_route): Error:', error));

        // https://echo.fbi.h-da.de/
        // https://api.group2.proxy.devops-pse.users.h-da.cloud
        // TODO: fetch data from web backend api(incomplete)
        /*const response = fetch('https://echo.fbi.h-da.de/',
        {
            method: 'GET',
            headers:
                {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json; charset=utf-8',
                    'Access-Control-Allow-Origin': '*',
                    'Sec-Fetch-Mode': 'cors'
                },
            mode: 'no-cors',
            body: post_body_data
        });*/

        return response_data;
    }

    /** Updates the HTML response section with the provided data.
     *
     * If the response section does not exist, it creates the section,
     * appends it to the body and displays the response data inside it.
     *
     * @param {string} data - The data to be displayed in the response section.
     */
    update_response_section(data) {
        "use strict";
        c_log('debug', '[Path_finder](update_response_section)');

        data = format_json(data);
        c_log('info', '[Path_finder](update_response_section): ', data);

        let response;

        if (document.getElementById("response") == null) {
            // Create section for response
            let section = document.createElement('section');
            section.id = "response_section";
            section.className = "flex_item";

            let footer = document.getElementsByTagName('footer')[0];
            document.getElementsByTagName('main')[0].appendChild(section);

            // Create a place to display the response
            response = document.createElement('p');
            response.id = "response";
            response.className = "flex1_item";
            response.innerText = data;

            section.appendChild(response);
        } else {
            response = document.getElementById('response');
        }

        response.innerText = data;
    }
}
