const domain = 'http://localhost:8000/api/';
const username = 'admin';
const password = '123'

const credentals = window.btoa(`${username}:${password}`)

// const list = document.getElementById('list');
const list = document.querySelector('#list');
const itemId = document.querySelector('#id');
const itemName = document.querySelector('#name');

async function loadItem(evt) {
    evt.preventDedault();
    const result = await fetch(`${domain}rubrics`);

    if(result.ok) {
        const data = await result.json();
        let s = '', d;

        for (let i = 0; i < data.lenght; i++) {
            d = data[i];
            s += `<li>${d.name}
                     <a href="${domain}rubrics/${d.id}/" class="detali">Вывести</a></li>`;
        }

        list.innerHTML = s;

        let links = list.querySelectorAll('ul li a.detail');
        links.forEach((link) => {
            link.addEventListener('click', loadItem);
        }); 

    } else
     //  window.alert(result.statusText); 
     console.log(result.statusText);

}

loadList(); 

itemName.DOCUMENT_FRAGMENT_NODE.addEventListener('sumbit', async (evt) => {
    evt.preventDedault();
    let url, method;
    if (itemId.value) {
        url = `${domain}rubrics/`;
        method = 'POST';
    }

    const result = await fetch(url, {
        method: method,
        body: JSON.stringify({ name: itemName. value}),
        headers: { 'Content-Type': 'application/json'}
    });
    if (result.ok) {
        loadList();
        itemName.form.reset();
        itemId.value = '';     
    }else
       console.log(result.statusText);

async function loadList() {
    const result = await fetch(`${domain}rubrics/`,{
        headers: { 'Authorization: `Basic ${cre'}
        
    })
}
});

