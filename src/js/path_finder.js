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
    c_log('info', '[Path_finder:global](Init)');

    try {
        //delete noscript-tag from page since js is working
        document.getElementById('noscript').remove();
        document.getElementById('script').remove();
    } catch (e) {
        c_log('error', "[Path_finder:global](Init): ", e);
    }

    // Object is necessary for the functionality of the page
    // noinspection JSUnusedLocalSymbols
    let path_finder = new Path_finder();

    if (TEST) {
        // write tests here
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
    c_log('info', '[Path_finder:global](is_valid_json)');

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
 * @returns {boolean} `true` if the JSON string is formatted (contains newlines and indentation),
 *                    and `false` if the string is compact (single-line).
 */
function is_formatted_json(jsonString) {
    "use strict";
    c_log('info', '[Path_finder:global](is_formatted_json)');

    return jsonString.includes('\n') && jsonString.includes('  ');
}

/** Formats the given JSON string to be more readable.
 *
 * @param {string|object} string - The string or object to be formatted.
 * @returns {string} The formatted JSON string with indentation for readability.
 */
function format_json(string) {
    "use strict";
    c_log('info', '[Path_finder:global](format_json)');

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
// noinspection JSUnusedGlobalSymbols
class Path_finder {

    // private class attributes
    /** Current disabled option of <select> endpoint
     *
     * @type {number}
     * if set on 0; nothing is disabled
     * @default 0
     * */
    #currently_disabled = 0;
    /** List of loaded cities
     *
     * @type {City[]}
     * @default {[]}
     */
    #cities = [];

    /** Binds methods to events/actions and
     * contains further configurations for class path_finder.
     */
    constructor() {
        "use strict";
        c_log('info', '[Path_finder](constructor)');

        try {
            // load cities for page initialization
            this.load_cities();

            // check completion of form with every change
            document.getElementById('path_points_form').oninput = this.check_form_completion.bind(this);
            // initial check of form completion
            this.check_form_completion();

            // makes sure, the user cannot select the same city as start- and endpoint
            document.getElementById('startpoint').onchange = this.disable_endpoint.bind(this);

            // deactivate reload of webpage
            document.getElementById('path_points_form').setAttribute('onsubmit', 'return false;');

            // process form data with a method instead of directly sending the form request
            document.getElementById('path_points_submit_button').onclick = this.process_form_data.bind(this);
        } catch (e) {
            c_log('error', '[Path_finder](constructor): ', e);
        }
    }

    /** searches list of cities for a city with given name
     *
     * @param {string} name
     *
     * @returns {City} `City` if city exists; otherwise `null`
     * */
    get_city_by_name(name) {
        "use strict";
        c_log('info', '[Path_finder](get_city_by_name)');

        for (let city of this.#cities) {
            if (name === city.get_name()) {
                return city;
            }
        }
        return null;
    }

    /** searches list of cities for a city with given coordinates
     *
     * @param {number} position_x
     * @param {number} position_y
     *
     * @returns {City} `City` if city exists; otherwise `null`
     * */
    get_city_by_coordinates(position_x, position_y) {
        "use strict";
        c_log('info', '[Path_finder](get_city_by_coordinates)');

        for (let city of this.#cities) {
            if (position_x === city.get_position_x() && position_y === city.get_position_y()) {
                return city;
            }
        }
        return null;
    }

    /** Fetches the cities from a backend api and saves them as city objects in the #cities attribute.
     *
     * @returns {string} -  A JSON string with only the names of the loaded cities
     */
    load_cities() {
        "use strict";
        c_log('info', '[Path_finder](load_cities)');

        /* Fetches the cities from the backend API.
         * response structure: map{"cities": [{...}, ...], "connections": [{...}, ...], "mapname": "..." }
         */
        fetch('http://localhost:5000/cities')
            .then(response => {
                if (!response.ok) {
                    throw new Error('[Path_finder](load_cities): Network problems: ' + response.statusText);
                }
                return response.json();
            })
            .then(map => {
                if (map.cities !== undefined) {
                    c_log('debug', '[Path_finder](load_cities) response: ', format_json(map));
                    const endpoint_list = document.getElementById('endpoint_list');
                    const select_startpoint = document.getElementById('startpoint');
                    const select_endpoint = document.getElementById('endpoint');

                    let counter = 0;

                    for (let city of map.cities) {
                        c_log('debug', '[Path_finder](load_cities): city: ', city.name);
                        this.#cities.push(new City(city.name, city.position_x, city.position_y));

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
                    }
                } else throw '[Path_finder](load_cities): Cities undefined';
            })
            .catch(error => c_log('error', '[Path_finder](load_cities): Error fetching cities: ', error));
    }

    /** Disables the city selected as startpoint for the endpoint selection
     */
    disable_endpoint() {
        "use strict";
        c_log('info', '[Path_finder](disable_endpoint)');

        let to_be_disabled = 0;

        let startpoint = document.getElementById('startpoint');
        for (let child of startpoint.children) {
            if (child.selected) {
                c_log('debug', '[Path_finder](disable_endpoint): startpoint set to ', child.getAttribute('value'), child.innerText);
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

    /** Checks if the form is filled out correctly.
     *
     * If both the start and endpoint are set,
     * the submit button is enabled;
     * otherwise, the button is disabled.
     */
    check_form_completion() {
        "use strict";
        c_log('info', '[Path_finder](check_form_completion)');

        try {
            let listItems = document.getElementById("path_points_form").childElementCount;
            let startpoint_is_set = !(document.getElementById("startpoint").value === "0" || document.getElementById("startpoint").value === "");
            let endpoint_is_set = !(document.getElementById("endpoint").value === "0" || document.getElementById("startpoint").value === "");
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
     * @async Due to Server communication.
     */
    async process_form_data() {
        "use strict";
        c_log('info', '[Path_finder](process_form_data)');

        let form_data = this.retrieve_form_data();
        c_log('debug', '[Path_finder](process_form_data): form_data: ', form_data);

        if (form_data === '') {
            return;
        }

        try {
            // await is necessary to wait for the response from the service
            // noinspection ES6RedundantAwait
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
     *   '{
     *      "startpoint": "Start City",
     *      "endpoint": "End City"
     *   }'
     *
     * @returns {string} A JSON string representing the selected `startpoint` and `endpoint` values.
     */
    retrieve_form_data() {
        "use strict";
        c_log('info', '[Path_finder](retrieve_form_data)');

        let form_data = {};

        // Retrieve form data
        let startpoint = document.getElementById('startpoint');
        for (let child of startpoint.children) {
            if (child.selected) {
                c_log('debug', '[Path_finder](retrieve_form_data): ', child.getAttribute('value'), ' ', child.innerText);
                form_data.startpoint = child.innerText;
            }
        }
        let endpoint = document.getElementById('endpoint');
        for (let child of endpoint.children) {
            if (child.selected) {
                c_log('debug', '[Path_finder](retrieve_form_data): ', child.getAttribute('value'), ' ', child.innerText);
                form_data.endpoint = child.innerText;
            }
        }

        if (form_data.startpoint === undefined || form_data.endpoint === undefined) {
            return '';
        } else if (form_data.startpoint === form_data.endpoint) {
            c_log("error", "[Path_finder](retrieve_form_data): Startpoint and endpoint are the same.");
            return '';
        }
        return format_json(form_data);
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
        c_log('info', '[Path_finder](get_route)');

        // Format the incoming request body if needed (you didn't provide the `format_json` function)

        let request_body_json = format_json(request_body)
        c_log('debug', '[Path_finder](get_route): request_body: ', request_body_json);

        let request_body_obj = JSON.parse(request_body_json);

        let response_data = {};
        let startpoint = request_body_obj.startpoint;
        let endpoint = request_body_obj.endpoint;
        let route = '';

        // Fetch the route from the API using the startpoint and endpoint from the request body
        await fetch(`http://localhost:5000/cities/route?startpoint=${startpoint}&endpoint=${endpoint}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('[Path_finder](get_route): Network problems: ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.route !== undefined) {
                    // Loop through the route array to build the route string
                    for (let i = 0; data.route[i.toString()]; i++) {
                        // Append each city to the route string
                        route += data.route[i.toString()] + ' => ';
                    }
                    // Remove the last ' => ' from the route string
                    route = route.substring(0, (route.length - ' => '.length));

                    // Construct the response data
                    response_data.route = 'Route from ' + startpoint + ' to ' + endpoint + ': ' + route + '.';
                    response_data.distance = 'The distance is ' + (parseFloat(data.distance).toFixed(2)).toString() + ' [units of length].';
                } else throw '[Path_finder](get_route): Route undefined';
            })
            .catch(error => {
                c_log('error', '[Path_finder](get_route): Error fetching route: ', error);
                response_data.error = 'Failed to fetch route data.';
            });

        return format_json(response_data);
    }


    /** Updates the HTML response section with the provided data.
     *
     * If the response section does not exist, it creates the section,
     * appends it into the main tag and displays the response data inside it.
     *
     * @param {string} data - The data to be displayed in the response section.
     */
    update_response_section(data) {
        "use strict";
        c_log('info', '[Path_finder](update_response_section)');

        data = format_json(data);
        c_log('debug', '[Path_finder](update_response_section): ', data);
        let response_data = JSON.parse(data);

        if (document.getElementById("response_article") == null) {
            // Create section for response_article
            let section = document.createElement('section');
            section.id = "response_section";
            section.className = "flex_item";

            document.getElementsByTagName('main')[0].appendChild(section);

            // Create an article for response paragraphs
            let article = document.createElement('article');
            article.id = "response_article";
            article.className = "flex6_container";

            section.appendChild(article);

            // Create a paragraph for the route
            let route_p = document.createElement('p');
            route_p.id = "route_p";
            route_p.className = "flex_item";
            route_p.innerText = response_data.route;

            article.appendChild(route_p);

            // Create a paragraph for the distance
            let distance_p = document.createElement('p');
            distance_p.id = "distance_p";
            distance_p.className = "flex_item";
            distance_p.innerText = response_data.distance;

            article.appendChild(distance_p);
        } else {
            document.getElementById('route_p').innerText = response_data.route;
            document.getElementById('distance_p').innerText = response_data.distance;
        }
    }
}

/** A class to save city information for easier handling
 * It handles following tasks:
 * - saving city information
 * - TODO: list tasks when class starts to be used
 */
// noinspection JSUnusedGlobalSymbols
class City {

    // private class attributes
    /** Name of the city
     * @default ''
     */
    #name;
    /** X coordinate of the city
     * @default 0
     */
    #position_x;
    /** Y coordinate of the city
     * @default 0
     */
    #position_y;

    /** Fills class attributes with given parameters
     *
     * @param {string} name
     * @param {number} position_x
     * @param {number} position_y
     *
     */
    constructor(name, position_x, position_y) {
        "use strict";
        c_log('info', '[City](constructor)');

        this.#name = name;
        this.#position_x = position_x;
        this.#position_y = position_y;
    }

    /** Getter for private class attribute name
     * @returns {string} name
     */
    get_name() {
        "use strict";
        c_log('info', '[City](get_name)');

        return this.#name;
    }

    /** Getter for private class attribute position_x
     * @returns {number} position_x
     */
    get_position_x() {
        "use strict";
        c_log('info', '[City](get_position_x)');

        return this.#position_x;
    }

    /** Getter for private class attribute position_y
     * @returns {number} position_y
     */
    get_position_y() {
        "use strict";
        c_log('info', '[City](get_position_y)');

        return this.#position_y;
    }

    /** Creates an unformatted JSON string of itself
     * @returns {string} - JSON formatted
     */
    to_json_string() {
        "use strict";
        c_log('info', '[City](to_json_string)');

        return JSON.stringify(this.to_json());
    }

    /** Creates a formatted JSON string of itself
     * @returns {string} - JSON formatted
     */
    to_formatted_json_string() {
        "use strict";
        c_log('info', '[City](to_formatted_json_string)');

        return format_json(this.to_json());
    }

    /** Creates a JSON object of itself
     * @returns {Object} - JSON object
     */
    to_json() {
        "use strict";
        c_log('info', '[City](to_json)');

        let self = {};
        self.name = this.#name;
        self.position_x = parseInt(this.#position_x);
        self.position_y = parseInt(this.#position_y);
        return JSON.parse(JSON.stringify(self));
    }
}
