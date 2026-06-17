// PAGE LOAD FADE

document.body.style.opacity = "0";

window.addEventListener("load",()=>{

    document.body.style.transition="1s";

    document.body.style.opacity="1";
});


/* PARALLAX */

document.addEventListener("mousemove",(e)=>{

    const x=e.clientX/window.innerWidth;
    const y=e.clientY/window.innerHeight;

    document.querySelectorAll(".tool-card")
    .forEach(card=>{

        card.style.transform=
        `
        rotateY(${(x-0.5)*10}deg)
        rotateX(${(0.5-y)*10}deg)
        `;
    });
});


/* SCROLL REVEAL */

const observer=new IntersectionObserver(entries=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.style.opacity="1";

            entry.target.style.transform=
            "translateY(0px)";
        }
    });

},{threshold:0.1});


document.querySelectorAll(".tool-card")
.forEach(card=>{

    card.style.opacity="0";

    card.style.transform=
    "translateY(50px)";

    card.style.transition="0.8s";

    observer.observe(card);
});


/* CURSOR GLOW */

const glow=document.createElement("div");

glow.classList.add("cursor-glow");

document.body.appendChild(glow);

glow.style.position="fixed";
glow.style.width="30px";
glow.style.height="30px";
glow.style.borderRadius="50%";

glow.style.background=
"rgba(96,165,250,0.35)";

glow.style.pointerEvents="none";

glow.style.filter="blur(15px)";

glow.style.zIndex="9999";


document.addEventListener("mousemove",(e)=>{

    glow.style.left=e.clientX-15+"px";

    glow.style.top=e.clientY-15+"px";
});

/* =========================
   APPLE NAVBAR SCROLL EFFECT
========================= */

window.addEventListener("scroll",()=>{

    const navbar =
    document.querySelector(".navbar");

    if(window.scrollY > 20){

        navbar.classList.add("scrolled");

    }else{

        navbar.classList.remove("scrolled");
    }
});

/* =========================
UPLOAD PREVIEW
========================= */

const fileInput =
document.getElementById("fileInput");

const previewBox =
document.getElementById("previewBox");

const previewImage =
document.getElementById("previewImage");

const fileName =
document.getElementById("fileName");

const fileSize =
document.getElementById("fileSize");

const dropZone =
document.getElementById("dropZone");

if(fileInput){

    /* FILE SELECT */

    fileInput.addEventListener("change",()=>{

        const file =
        fileInput.files[0];

        if(file){

            previewBox.style.display =
            "flex";

            previewImage.src =
            URL.createObjectURL(file);

            fileName.innerText =
            file.name;

            fileSize.innerText =
            (file.size / 1024 / 1024)
            .toFixed(2) + " MB";
        }
    });

    /* DRAG EFFECT */

    ["dragenter","dragover"]
    .forEach(eventName=>{

        dropZone.addEventListener(
            eventName,
            e=>{

                e.preventDefault();

                dropZone.style.borderColor =
                "#8b5cf6";

                dropZone.style.transform =
                "scale(1.02)";
            }
        );
    });

    ["dragleave","drop"]
    .forEach(eventName=>{

        dropZone.addEventListener(
            eventName,
            e=>{

                e.preventDefault();

                dropZone.style.borderColor =
                "rgba(255,255,255,0.2)";

                dropZone.style.transform =
                "scale(1)";
            }
        );
    });

    /* DROP FILE */

    dropZone.addEventListener(
        "drop",
        e=>{

            const file =
            e.dataTransfer.files[0];

            fileInput.files =
            e.dataTransfer.files;

            previewBox.style.display =
            "flex";

            previewImage.src =
            URL.createObjectURL(file);

            fileName.innerText =
            file.name;

            fileSize.innerText =
            (file.size / 1024 / 1024)
            .toFixed(2) + " MB";
        }
    );
}

/* =========================
3D CARD INTERACTION
========================= */

document.querySelectorAll(".tool-card")
.forEach(card=>{

    card.addEventListener(
        "mousemove",
        e=>{

            const rect =
            card.getBoundingClientRect();

            const x =
            e.clientX - rect.left;

            const y =
            e.clientY - rect.top;

            const centerX =
            rect.width / 2;

            const centerY =
            rect.height / 2;

            const rotateX =
            ((y - centerY) / 18);

            const rotateY =
            ((centerX - x) / 18);

            card.style.transform =
            `
            perspective(1000px)
            rotateX(${rotateX}deg)
            rotateY(${rotateY}deg)
            translateY(-10px)
            scale(1.03)
            `;
        }
    );

    card.addEventListener(
        "mouseleave",
        ()=>{

            card.style.transform =
            `
            perspective(1000px)
            rotateX(0deg)
            rotateY(0deg)
            translateY(0px)
            scale(1)
            `;
        }
    );
});

/* =========================
APPLE LOADER
========================= */

window.addEventListener("load",()=>{

    const loader =
    document.getElementById("loader");

    setTimeout(()=>{

        loader.classList.add("hide");

    },2500);
});

/* =========================
MOUSE SPOTLIGHT
========================= */

const mouseLight =
document.querySelector(".mouse-light");

document.addEventListener(
    "mousemove",
    e=>{

        mouseLight.style.left =
        e.clientX + "px";

        mouseLight.style.top =
        e.clientY + "px";
    }
);

/* =========================
NEURAL NETWORK
========================= */

const canvas =
document.getElementById("neuralCanvas");

const ctx =
canvas.getContext("2d");

canvas.width =
window.innerWidth;

canvas.height =
window.innerHeight;

const particles = [];

for(let i=0;i<70;i++){

    particles.push({

        x:Math.random()*canvas.width,

        y:Math.random()*canvas.height,

        vx:(Math.random()-0.5)*1,

        vy:(Math.random()-0.5)*1
    });
}

function animateNeural(){

    ctx.clearRect(
        0,0,
        canvas.width,
        canvas.height
    );

    particles.forEach(p=>{

        p.x += p.vx;
        p.y += p.vy;

        if(p.x<0 || p.x>canvas.width)
            p.vx *= -1;

        if(p.y<0 || p.y>canvas.height)
            p.vy *= -1;

        ctx.beginPath();

        ctx.arc(
            p.x,p.y,
            2,0,
            Math.PI*2
        );

        ctx.fillStyle =
        "rgba(96,165,250,0.7)";

        ctx.fill();

        particles.forEach(p2=>{

            const dist =
            Math.hypot(
                p.x-p2.x,
                p.y-p2.y
            );

            if(dist<120){

                ctx.beginPath();

                ctx.moveTo(p.x,p.y);

                ctx.lineTo(p2.x,p2.y);

                ctx.strokeStyle =
                `rgba(168,85,247,${
                    1-dist/120
                })`;

                ctx.stroke();
            }
        });
    });

    requestAnimationFrame(
        animateNeural
    );
}

animateNeural();