$(function() {

    $('#add-cupcake-form').on('submit', async function(evt){
        evt.preventDefault();
        const flavor = $('#flavor').val()
        const size = $('#size').val()
        const rating = $('#rating').val()
        const img = $('#url').val()
        let response = await $.ajax({
            method: "POST",
            url: `/cupcakes`,
            contentType: "application/json",
            data: JSON.stringify({
                flavor,
                size, 
                rating, 
                img
            }),
          });
        
    })
})
