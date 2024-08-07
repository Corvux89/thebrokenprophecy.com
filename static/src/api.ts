import { Adventure, CategoryClass, Character, Item, PlayerClass, Races } from "./types.js";

export function getAdventures(): Promise<Adventure[]>{
    return fetch(`${window.origin}/api/adventures`)
    .then(res => res.json())
    .then(res => {
        return res as Adventure[]
    })
}

export function getCharacters(): Promise<Character[]>{
    return fetch(`${window.origin}/api/characters`)
    .then(res => res.json())
    .then(res => {
        return res as Character[]
    })
}

export function getRaces(): Promise<Races[]>{
    return fetch(`${window.origin}/api/races`)
    .then(res => res.json())
    .then(res => {
        return res as Races[]
    })
}

export function getClasses(): Promise<PlayerClass[]>{
    return fetch(`${window.origin}/api/classes`)
    .then(res => res.json())
    .then(res => {
        return res as PlayerClass[]
    })
}

export function getAllItems(): Promise<Item[]>{
    return fetch(`${window.origin}/api/items`)
    .then(res => res.json())
    .then(res => {
        return res as Item[]
    })
}

export function getItem(table: string, item: number): Promise<Item>{
    return fetch(`${window.origin}/api/items/${table}/${item}`)
    .then(res => res.json())
    .then(res => {
        return res as Item
    })
}

export function updateItem(item: Item): Promise<Item>{
    return new Promise((resolve, reject) => {
        const request = new XMLHttpRequest()

        request.open('PATCH', `/api/items`, true)
        request.setRequestHeader('Content-Type', 'application/json')

        request.onload = function () {
            if (request.status == 200){
                resolve(this.response.responseText)
            } else {
                resolve(null)
            }
        }

        request.onerror = function () {
            reject(new Error("Something went wrong"))
        }

        request.send(JSON.stringify(item))
    })
}

export function getRarities(): Promise<CategoryClass[]>{
    return fetch(`${window.origin}/api/rarity`)
    .then(res => res.json())
    .then(res => {
        return res as CategoryClass[]
    })
}

export function getItemTypes(table: string): Promise<CategoryClass[]>{
    return fetch(`${window.origin}/api/item_type/${table}`)
    .then(res => res.json())
    .then(res => {
        return res as CategoryClass[]
    })
}

export function getMagicSchools(): Promise<CategoryClass[]>{
    return fetch(`${window.origin}/api/magic_schools`)
    .then(res => res.json())
    .then(res => {
        return res as CategoryClass[]
    })
}