export function getAdventures() {
    return fetch(`${window.origin}/api/adventures`)
        .then(res => res.json())
        .then(res => {
        return res;
    });
}
