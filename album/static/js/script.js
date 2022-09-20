

function deleteAlbum(e) {
    e.preventDefault();
    fetch(window.location.href, {method: 'DELETE'}).then(r=> {
        if(r.status === 204) {
            let modalBody = document.getElementById('modalBody')
            modalBody.className = "alert alert-success" 
            modalBody.innerText = "Success: Album deleted successfully, redirecting..."
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
        modalBody.className = "alert alert-success"
        modalBody.innerText = "Success: Photo deleted successfully, redirecting..."
        setTimeout(()=> {
            redirectUrl = url.substring(0, url.lastIndexOf('/'));
            setTimeout(() => window.location = redirectUrl, 2000)
        })

        }
        
    })
}

function main() {
    if (document.getElementById('deleteAlbumButton') != null ){
        document.getElementById('deleteAlbumButton').onclick = e => deleteAlbum(e);
    }

    if (document.getElementById('deletePhotoButton') != null) {
        document.getElementById('deletePhotoButton').onclick = e => deletePhoto(e);
    }
}

main()