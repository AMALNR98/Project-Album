

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
        .catch(e => console.log(e))
}

function publishAlbum() {
    fetch(document.location.href, {
        method: 'put',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'publish': true})
    })
    .then((r) => {
        if (r.status === 204) {
            document.getElementById("publishModalTitle").innerText = "Success"
            document.getElementById("publishModalBody").className = "alert alert-success";
            document.getElementById("publishModalBody").innerText = "album published successfully,reloading";
            setTimeout(()=>window.location = window.location, 1200);
        }
    })


}

function copyPublickLink(e) {
    navigator.clipboard.writeText(document.location.href).then(()=> console.log('album link copied successfully'))
    document.getElementById("tooltipSpan").innerText = "copied"
    setTimeout(()=>{
        document.getElementById("tooltipSpan").innerText = "copy"
    }, 1000)
}

function addPostComment(e)  {
    if (e.key == "Enter") {
        let displayName = "sanju";
        let commentText = "this is a comment";
        let commentDate = "24-03-1998";
        let commentCard = document.createElement("div");
        commentCard.className = "card mb-3"
        commentCard.innerHTML = `<div class="card-body">
            <div class="d-flex flex-start">
              <img class="rounded-circle shadow-1-strong me-3"
                src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(26).webp" alt="avatar" width="40"
                height="40" />
              <div class="w-100">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h6 id="displayName" class="text-primary fw-bold mb-0 displayName">
                    <span id="commentText" class="commentText text-dark ms-2">comment</span>
                  </h6>
                  <p id="commentDate" class="mb-0 commentDate">date</p>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                  <p class="small mb-0" style="color: #aaa;">
                    <a href="#!" class="link-grey">Remove</a> •
                    <a href="#!" class="link-grey">Reply</a> •
                    <a href="#!" class="link-grey">Translate</a>
                  </p>
                  <div class="d-flex flex-row">
                    <i class="fas fa-star text-warning me-2"></i>
                    <i class="far fa-check-circle" style="color: #aaa;"></i>
                  </div> </div>
              </div>
            </div>
          </div>`
        fetch(window.location.href + "/comment", {
            method: 'POST',
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'},
            body: JSON.stringify({'comment': document.getElementById("commentInput").value})}
            )
            .then( r => r.json())
            .then( json => {

                commentCard.getElementsByClassName('displayName')[0].innerText = json.display_name;
                let commentSpan = document.createElement('span');
                commentSpan.className = "text-dark ms-2";
                commentSpan.innerText = json.comment;
                commentCard.getElementsByClassName('displayName')[0].appendChild(commentSpan)
                commentCard.getElementsByClassName('commentDate')[0].innerText = "now";
                document.getElementById('commentParent').prepend(commentCard);
                document.getElementById("commentInput").value = ""

            }).catch(e => console.log(e))

        

    }
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

    if (document.getElementById("copyLinkButton") != null) {
        
        document.getElementById("copyLinkButton").onclick = e => copyPublickLink(e);
    }

    if (document.getElementById("commentInput") !=  null){
        document.getElementById("commentInput").addEventListener("keyup", (e)=> addPostComment(e))
    }
}

main()