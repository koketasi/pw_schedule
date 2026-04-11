const edit_func=(rowid)=>{
    const card=document.getElementById(`card-${rowid}`);
    card.querySelector('.view').style.display='none';
    card.querySelector('.edit').style.display='block';
}
const view_func=(rowid)=>{
    const card=document.getElementById(`card-${rowid}`);
    card.querySelector('.edit').style.display='none';
    card.querySelector('.view').style.display='flex';
}

const now=new Date();
const year_current=now.getFullYear();
const month_current=now.getMonth()+1;
const day_current=now.getDate();
const minute_current=now.getMinutes();
const hour_current=now.getHours();
const week=['日','月','火','水','木','金','土'];



const years=document.querySelectorAll("select[name='year']");
const months=document.querySelectorAll("select[name='month']");
const days=document.querySelectorAll("select[name='day']");
const hours=document.querySelectorAll("select[name='hour']");
const minutes=document.querySelectorAll("select[name='minute']");
const dates=document.querySelectorAll(".date");


years.forEach((year,index)=>{
    for(let i=2026;i<=2070;i++){
        let year_option=document.createElement('option');
        year_option.value=i;
        year_option.textContent=i;
        year.appendChild(year_option);
        
    }
    if(index==0){
        year.value=year_current;
    }
    else{
        year.value =Number( year.getAttribute('data-value'));
    }
});

months.forEach((month,index)=>{
    for(let i=1;i<=12;i++){
        let month_option=document.createElement('option');
        month_option.value=i;
        month_option.textContent=i;
        month.appendChild(month_option);
        
    }
    if(index==0){
        month.value=month_current;
    }
    else{

        month.value =Number( month.getAttribute('data-value'));
    }
});

days.forEach((day,index)=>{
    for(let i=1;i<=31;i++){
        let day_option=document.createElement('option');
        day_option.value=i;
        day_option.textContent=i;
        day.appendChild(day_option);
        
    }
    if(index==0){
        day.value=day_current;
    }
    else{
        day.value =  Number(day.getAttribute('data-value'));
    }
    
});
hours.forEach((hour,index)=>{
    for(let i=0;i<=23;i++){
        let hour_option=document.createElement('option');
        hour_option.value=i;
        hour_option.textContent=i;
        hour.appendChild(hour_option);
        
    }
    if(index==0){
        if (55<=minute_current && minute_current<=59){
            hour.value=hour_current+1;
        }
        else{
            hour.value=hour_current;
        }
    }
    else{
        hour.value =  Number(hour.getAttribute('data-value'));
    }
    
});
minutes.forEach((minute,index)=>{
    for(let i=0;i<=55;i+=5){
        let minute_option=document.createElement('option');
        
        minute_option.value=String(i).padStart(2,'0');
        minute_option.textContent=String(i).padStart(2,'0');
        minute.appendChild(minute_option);
        
    }
    if(index>=1){
        minute.value =  minute.getAttribute('data-value');
    }

});
dates.forEach((date)=>{
    card=date.closest('.card');
    id=card.id.replace('card-','');
    
    content=date.textContent;
    date_year=parseInt(content);//数値以外が来たら読み取らない
    date_month=parseInt(content.split('年')[1]);
    date_day=parseInt(content.split('月')[1]);
    week_Day=new Date(date_year,date_month-1,date_day);
    week_day=week[week_Day.getDay()];

    document.getElementById(`week-${id}`).textContent=`(${week_day})`;
});


