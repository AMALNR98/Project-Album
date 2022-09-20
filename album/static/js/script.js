

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

function main() {
    document.getElementById('deleteAlbumButton').onclick = e => deleteAlbum(e);
}

main()