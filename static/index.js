document.addEventListener('DOMContentLoaded', nav)

function nav(){

	const search_id = document.getElementById('search_id');
	const btn_search = document.querySelector('button');

	btn_search.addEventListener("click",e=>{
		recipe = search_id.value.trim()
		if(recipe=="") document.location.href = `/`
		else document.location.href = `/?recipe=${recipe}`
	})

}

function $_GET(param) {
	var vars = {};
	window.location.href.replace( location.hash, '' ).replace( 
		/[?&]+([^=&]+)=?([^&]*)?/gi, // regexp
		function( m, key, value ) { // callback
			vars[key] = value !== undefined ? value : '';
		}
	);

	if ( param ) {
		return vars[param] ? vars[param] : null;	
	}
	return vars;
}