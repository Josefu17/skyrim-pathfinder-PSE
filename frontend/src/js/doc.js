window.onload = Init;
require('https://cdn.jsdelivr.net/npm/marked/marked.min.js');

async function Init() {
    'use strict';

    try {
        // delete (no-)script-tag from page
        // convert iteration into array to prevent changing iteration by
        // removing the current item and thus losing the next item
        for (let item of Array.from(document.getElementsByClassName('deleted_by_js'))) {
            item.remove();
        }

        // convert .md file into html and write into element with id "documentation"
        await fetch('../project_information/Doku.md')
            .then((response) => response.text())
            .then(
                (text) => (document.getElementById('documentation').innerHTML = marked.parse(text))
            )
            .then(() => {
                set_anchor_targets();
            });
    } catch (e) {
        console.log('[Init]: ', e);
    }
}

/** sets all anchor-targets to enable referencing between elements
 */
function set_anchor_targets() {
    'use strict';

    let references = document.getElementsByTagName('a');
    for (let reference of references) {
        let ref_str = reference.href.replace(
            /https:\/\/group2.proxy.devops-pse.users.h-da.cloud\/doc.html/g,
            ''
        );
        ref_str = ref_str.replace(/http:\/\/localhost:63342\/Doku.md\/src\/doc.html/g, '');
        let is_set = false;
        is_set = set_anchor_target(ref_str, 'h1');
        if (!is_set) {
            is_set = set_anchor_target(ref_str, 'h2');
        }
        if (!is_set) {
            is_set = set_anchor_target(ref_str, 'h3');
        }
    }
}

/**
 * @param {string} reference
 * @param {'h1'} tag_name
 * @param {'h2'} tag_name
 * @param {'h3'} tag_name
 *
 * @returns ```true``` if anchor target was set; otherwise ```false```.
 * */
function set_anchor_target(reference, tag_name) {
    'use strict';

    let h_list = document.getElementsByTagName(tag_name);
    for (let h of h_list) {
        let string = '#' + replaceSpecialChars(h.textContent);
        if (string === reference) {
            h.id = string.replace('#', '');
            return true;
        }
    }
    return false;
}

function replaceSpecialChars(inputString) {
    return inputString
        .replace(/\//g, '') // replace '/' with ''
        .replace(/ /g, '-') // replace ' ' with '-'
        .replace(/\W/g, '-') // replace all non-word characters with '-'
        .toLowerCase();
}
