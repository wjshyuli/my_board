document.addEventListener("DOMContentLoaded", function () {

    const summary = document.querySelector(".summary");

    if (!summary) return;

    let pauseUntil = 0;

    function pauseAutoScroll() {
        pauseUntil = Date.now() + 5000; // 暂停5秒
    }

    // 鼠标操作
    summary.addEventListener("mousedown", pauseAutoScroll);
    summary.addEventListener("wheel", pauseAutoScroll);

    // 触摸屏
    summary.addEventListener("touchstart", pauseAutoScroll);
    summary.addEventListener("touchmove", pauseAutoScroll);

    setInterval(() => {

        if (Date.now() < pauseUntil) {
            return;
        }

        summary.scrollLeft += 1;

        if (
            summary.scrollLeft >=
            summary.scrollWidth - summary.clientWidth
        ) {
            summary.scrollLeft = 0;
        }

    }, 30);

});

// 点击机台显示具体状态模块
let currentMachine=null
let machine_list=[
    {"machineNo":"3H101","status":"生产","spec":"PCR001","qty":1250}
]
function showDetail(machineNo){
    console.log('click machine');
    const panel = document.getElementById("detail_panel_id1")

    if(currentMachine === machineNo){
        console.log('click machine agian');
        
        panel.classList.remove('show');
        currentMachine = null;
        return;
    }
    currentMachine = machineNo
    panel.classList.add("show")
    //从本地数组找数据
    console.log(machineList)
    const machine =machineList.find(item => item.machineNo===machineNo)
    const data =machine || {
        machineNo:"no",
        status:"no",
        spec:"no",
        qty:"no",
    }
    document.getElementById("machineName").innerText=data.machineNo;
    document.getElementById("status").innerText=data.status;
    document.getElementById("spec").innerText=data.spec;
    document.getElementById("qty").innerText=data.qty;  
};

function closePanel(){
    const panel =document.getElementById("detail_panel_id1")
    panel.classList.remove("show");
    currentMachine=null;
    console.log("click card to close");
    

};
