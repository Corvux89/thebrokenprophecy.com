import { Adventure } from "./types.js";

export function getAdventures(): Promise<Adventure[]>{
    return fetch(`${window.origin}/api/adventures`)
    .then(res => res.json())
    .then(res => {
        return res as Adventure[]
    })
}