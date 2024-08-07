export function getAdventures() {
    return fetch(`${window.origin}/api/adventures`)
        .then(res => res.json())
        .then(res => {
        return res;
    });
}
export function getCharacters() {
    return fetch(`${window.origin}/api/characters`)
        .then(res => res.json())
        .then(res => {
        return res;
    });
}
export function getRaces() {
    return fetch(`${window.origin}/api/races`)
        .then(res => res.json())
        .then(res => {
        return res;
    });
}
export function getClasses() {
    return fetch(`${window.origin}/api/classes`)
        .then(res => res.json())
        .then(res => {
        return res;
    });
}
export function getAllItems() {
    return fetch(`${window.origin}/api/items`)
        .then(res => res.json())
        .then(res => {
        return res;
    });
}
export function getItem(table, item) {
    return fetch(`${window.origin}/api/items/${table}/${item}`)
        .then(res => res.json())
        .then(res => {
        return res;
    });
}
export function updateItem(item) {
    return new Promise((resolve, reject) => {
        const request = new XMLHttpRequest();
        request.open('PATCH', `/api/items`, true);
        request.setRequestHeader('Content-Type', 'application/json');
        request.onload = function () {
            if (request.status == 200) {
                resolve(this.response.responseText);
            }
            else {
                resolve(null);
            }
        };
        request.onerror = function () {
            reject(new Error("Something went wrong"));
        };
        request.send(JSON.stringify(item));
    });
}
export function getRarities() {
    return fetch(`${window.origin}/api/rarity`)
        .then(res => res.json())
        .then(res => {
        return res;
    });
}
export function getItemTypes(table) {
    return fetch(`${window.origin}/api/item_type/${table}`)
        .then(res => res.json())
        .then(res => {
        return res;
    });
}
export function getMagicSchools() {
    return fetch(`${window.origin}/api/magic_schools`)
        .then(res => res.json())
        .then(res => {
        return res;
    });
}
