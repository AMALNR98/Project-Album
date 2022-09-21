

function deleteAlbum(e) {
    e.preventDefault();
    fetch(window.location.href, {method: 'DELETE'}).then(r=> {
        if(r.status === 204) {
            let modalBody = document.getElementById('modalBody')
            modalBody.className = "alert alert-success" 
            modalBody.innerText = "Success: Album deleted successfully, redirecting..."
            let modalTitle = document.getElementById('modalTitle');
            modalTitle.innerText = "Success";
            setTimeout(() => window.location = '/', 2000)
            e.target.disabled = true
        }
    })

}

function deletePhoto(e) {
    console.log('something')
    e.preventDefault();
    let url = window.location.href;
    fetch(url, {method: 'DELETE'})
    .then(r => {
        if (r.status == 204) {
        let modalBody = document.getElementById('modalBody');
        modalBody.className = "alert alert-success";
        modalBody.innerText = "Success: Photo deleted successfully, redirecting...";
        let modalTitle = document.getElementById('modalTitle');
            modalTitle.innerText = "Success";
       
        setTimeout(()=> {
            redirectUrl = url.substring(0, url.lastIndexOf('/'));
            setTimeout(() => window.location = redirectUrl, 2000)
        })

        }
        
    })
}

function likeDislike() {
    let icon = photoLikeButton.querySelector('.heartIcon');
    if(localStorage.getItem("likeStatus" + icon.id) == "false") {
        getLikeResponse(true, icon)
    }
    else {
        getLikeResponse(false, icon)
    }
}

function getLikeResponse(status, icon) {
    fetch(document.location.href, {
        method: 'put',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'like': status})
    })
        .then(r => r.json())
        .then(json => {
            if(status == true){
                icon.innerText = ` ${json.likes}`
                icon.style.color = "red";
                localStorage.setItem("likeStatus" + icon.id, "true")
            }
            else {
                icon.innerText = ` ${json.likes}`
                icon.style.color = "";
                localStorage.setItem("likeStatus" + icon.id, "false")
            }
               
        })
}

function publishAlbum() {
    fetch(document.location.href, {
        method: 'put',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'publish': true})
    }).then((r)=> console.log('meh',r))

}

function main() {
    if (document.getElementById('deleteAlbumButton') != null ){
        document.getElementById('deleteAlbumButton').onclick = e => deleteAlbum(e);
    }

    if (document.getElementById('deletePhotoButton') != null) {
        document.getElementById('deletePhotoButton').onclick = e => deletePhoto(e);
    }
    if (document.getElementById('photoLikeButton') != null ){
        let photoLikeButton = document.getElementById('photoLikeButton');
        let icon = photoLikeButton.querySelector('.heartIcon')
        if (localStorage.getItem("likeStatus" + icon.id) == null ) {
            localStorage.setItem("likeStatus" + icon.id, false)
        }
        if (localStorage.getItem("likeStatus" + icon.id) == "true" ) {

            icon.style.color = "red";
        }
        if (localStorage.getItem("likeStatus" + icon.id) == "false" ) {
            console.log('inside true')
            icon.style.color = "";
        }
        document.getElementById('photoLikeButton').onclick = e => likeDislike(e);
    }

    if (document.getElementById('publishAlbumButton') != null ) {
        document.getElementById('publishAlbumButton').onclick = e => publishAlbum(e);
    }
}

main()