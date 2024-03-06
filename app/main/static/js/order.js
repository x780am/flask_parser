document.addEventListener('DOMContentLoaded', function() { 
    
    setTimeout(function(){
        location = ''
    }, 90000) //10000 = 10 сек

    if (order_status_id > 0){
        document.getElementById('progress_work').style.display = "block";
        document.getElementById('progressbar_work').innerHTML = progressbar_work_text; 
        document.getElementById('progressbar_work').style = 'width: ' + progressbar_work_coord + '%;height: 20px;';

        if (order_status_id == 4){
            document.getElementById('progress_ads').style.display = "none";
            document.getElementById('progressbar_ads').innerHTML = '';
            document.getElementById('progressbar_ads').style = 'width: 0%;height: 20px;';
        }
        else{
            document.getElementById('progress_ads').style.display = "block";
            document.getElementById('progressbar_ads').innerHTML = progressbar_ads_text;                
            document.getElementById('progressbar_ads').style = 'width: ' + progressbar_ads_coord + '%;height: 20px;';
        }
    }
    else{
        document.getElementById('progress_ads').style.display = "none";
        document.getElementById('progress_work').style.display = "none";
    }
}, false);

function order_repeat(hash){
    alert('order_repeat');
    //document.location.href = 'https://parser24.online/avito_parser?hash_repeat='+hash;
};

