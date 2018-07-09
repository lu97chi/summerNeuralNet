$(document).ready(function () {
    $('select').formSelect();
    $('.modal').modal();
    $('.sidenav').sidenav();
});

let $avg = $('#avg').on('input', (e)=>{
    let val = parseInt($('#avg').val())
    $('#maxS').val(val * 1.2)
});
let form = new FormData();
let dataRes = false;
let traffic;
let loading;
let $send = document.getElementById('send').addEventListener('click', () => {
    let $year = $('#year').val()
    let $month = $('#month').val()
    let $direction = $('#direction').val();
    let $speedL = $('#speedL').val();
    let $time = $('#time').val();
    let $cars = $('#cars').val();
    let $day = $('#day').val();
    let $street = $('#street').val();
    let $max = $('#maxS').val();
    let $avg = $('#avg').val();
    form.set('year', $year)
    form.set('month', $month)
    form.set('direction', $direction)
    form.set('speedLimit', $speedL)
    form.set('time', $time)
    form.set('cars', $cars)
    form.set('day', $day)
    form.set('type',$street)
    form.set('vp', $avg)
    form.set('vm', $max)
    if($speedL && ($time && $time < 24) && $cars){
        fetch('https://neuraltesttrain.herokuapp.com/api/proto2', {
        // fetch('http://localhost:9000/api/proto2', {
        method: 'POST',
        body: form
            })
        .then(data => data.json()).then(data => {
            console.log(data.response)
            dataRes = true;
            if(data.response){
                $('#loader').hide()
                $('#trafficValue').text('Habra Trafico :c')
                traffic = true;                
            }else{
                $('#loader').hide()
                $('#trafficValue').text('No habra Trafico :D')
                traffic = false;                
            }
        })
    }
})

$('#saveFeedGood').on('click', ()=>{
    form.set('traffic', traffic)
    form.set('feedBack',true)
    if(dataRes){
        fetch('https://neuraltesttrain.herokuapp.com/api/db',{
            // fetch('http://localhost:9000/api/db', {

        method: 'POST',
        body: form
        }).then(data => data.json()).then( data => {
            console.log(data)
        })
    }
})

$('#saveFeedBad').on('click', ()=>{
    form.set('traffic', traffic)
    form.set('feedBack', false)
    if(dataRes){
        fetch('https://neuraltesttrain.herokuapp.com/api/db',{
            // fetch('http://localhost:9000/api/db', {

        method: 'POST',
        body: form
        }).then(data => data.json()).then( data => {
            console.log(data)
        })
    }
})

