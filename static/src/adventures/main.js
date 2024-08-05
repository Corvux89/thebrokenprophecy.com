import { getAdventures } from "../api.js";
getAdventures()
    .then(adventures => {
    let adventure_body = document.getElementById("adventure-table-body");
    adventures.forEach(a => {
        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${a.name}</td>
            <td class="text-center">${a.tier}</td>
            <td>${a.dms.join(', ')}</td>
            <td>${a.players.join(', ')}</td>
        `;
        adventure_body.appendChild(row);
    });
    $("#spinner").addClass("hidden");
    alert("done");
});
