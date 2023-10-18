const base_url = "http://localhost:8001"

window.addEventListener('load', () => {
    get_all_news()
  });


function ref(){
    const news = document.getElementById("news-items")
    news.replaceChildren()
}

const get_news = e => {
    ref();
    const news_id = e.target.id
    fetch(base_url+"/news?doc_id="+news_id, {method: "GET"})
    .then(response => {
        if (!response.ok){
            throw new Error("Ответ херовый")
        }
        return response.json()
    })
    .then(data => {
        const newsContainer = document.querySelector('.news');

        data.news.forEach(item => {
            const newsItem = document.createElement('div');
            const nitem = create_item(newsItem, item, true);
            newsContainer.appendChild(nitem);
        });
    })
}

function create_item(newsItem, item, details){
    if (details == true){
        newsItem.className = 'news-item-details';
        
        const title = document.createElement('h2');
        title.textContent = item.title;
        newsItem.appendChild(title);

        const details = document.createElement('div');
        details.textContent = item.description;
        newsItem.appendChild(details);
    }else{
        newsItem.className = 'news-item';
    
        const title = document.createElement('input');
        title.value = item.title;
        title.type = "button"
        title.id = item.id
        title.onclick = get_news
        newsItem.appendChild(title);
    
        const delete_btn = document.createElement('input');
        delete_btn.value = "X";
        delete_btn.id = item.id;
        delete_btn.type = "button"
        delete_btn.className = "del-btn"
        delete_btn.onclick = del_btn
        newsItem.appendChild(delete_btn);
    
        const date_container = document.createElement('div')
        date_container.className = "date_container"
    
        const date = document.createElement('p');
        date.textContent = item.date + " "+ item.time;
        date_container.appendChild(date);
    
        newsItem.appendChild(date_container)
    }

    return newsItem
}


function get_all_news(){
    ref();
    fetch(base_url + '/news/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const newsContainer = document.querySelector('.news');

            if (data.news.length == 0){
                const emptyRes = document.createElement('p')
                emptyRes.textContent = "Новостей пока нема"
                emptyRes.className = "title"
                newsContainer.appendChild(emptyRes)
            }

            data.news.forEach(item => {
                const newsItem = document.createElement('div');
                const nitem = create_item(newsItem, item, false);
                newsContainer.appendChild(nitem);
            });
        })
        .catch(error => {
            console.log('There was a problem with the fetch operation:', error.message);
        });
    }



function find_news(){
    ref();
    const find_str = document.getElementById("FindNews_inp").value;
    fetch(base_url + "/news?find_str=" + find_str)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const newsContainer = document.querySelector('.news');

        if (data.news.length == 0){
            const emptyRes = document.createElement('p')
            emptyRes.textContent = "По такому запросу ничего не найдено"
            emptyRes.className = "title"
            newsContainer.appendChild(emptyRes)
        }

        data.news.forEach(item => {
            const newsItem = document.createElement('div');
            const nitem = create_item(newsItem, item);
            newsContainer.appendChild(nitem);
        });
    })
    .catch(error => {
        console.log('There was a problem with the fetch operation:', error.message);
    });
}


const del_btn = e => {
    const news_id = e.target.id
    fetch(base_url+"/news?id="+news_id, {method: "DELETE"})
    .then(response => {
        if(!response.ok){
            throw new Error('Network response was not ok');
        }
        return response.json()
    })
    setTimeout(() => { get_all_news() }, 2000);
}


function create_new(){
    const data = {
        title: "string",
        description: "string",
        date: "string",
        time: "string",
    }
    const title = document.getElementById("new-title").value
    const description = document.getElementById("new-description").value
    const date = document.getElementById("new-date").value
    const time = document.getElementById("new-time").value
    
    const current_date = new Date();
    let currentDay= String(current_date.getDate()).padStart(2, '0');
    let currentMonth = String(current_date.getMonth()+1).padStart(2,"0");
    let currentYear = current_date.getFullYear();
    let currentHours = current_date.getHours();
    let currentMinutes = current_date.getMinutes();

    let currentDate = `${currentDay}.${currentMonth}.${currentYear}`
    let currentTime = `${currentHours}:${currentMinutes}`

    data.title = title != "" ? title : "string"
    data.description = description != "" ? description : "string"
    data.date = date != "" ? date : currentDate
    data.time = time != "" ? time : currentTime
    console.log(data)
    fetch(`${base_url}/new_news/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
          },
        body: JSON.stringify(data)
    })
    
    setTimeout(() => { get_all_news() }, 2000)
}


function AddNews(){
    ref();
    const newsItems = document.querySelector(".news")
    const form = document.createElement("div")
    form.className = "create-news-form"
    const formInner = document.createElement("div")
    formInner.className = "create-news-form-inner"

    fields = ["title", "description"]

    fields.forEach(field => {
        const label = document.createElement('label');
        label.textContent = null;
            
        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = field;
        input.id = `new-${field}`
        input.className = "form-inp"
            
        label.appendChild(input);
        formInner.appendChild(label);
            
        const br = document.createElement('br');
        formInner.appendChild(br);
    })
    const submitButton = document.createElement('input');
    submitButton.type = 'button';
    submitButton.className = 'form-btn';
    submitButton.onclick = create_new;
    submitButton.value = 'Создать';
    
    formInner.appendChild(submitButton)
    form.appendChild(formInner);
    newsItems.appendChild(form)
}