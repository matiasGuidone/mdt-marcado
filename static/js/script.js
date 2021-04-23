
function borrarJS(dir) {
    let id = document.getElementById('ide')['value'];
    var formData = new FormData();
    formData.append("id", id);
    let xhr = new XMLHttpRequest();
    let URLactual = window.location;
    xhr.open('DELETE', URLactual.origin + '/' + dir, true);
    xhr.onreadystatechange = function (aEvt) {
        if (xhr.readyState == 4) {
            if (xhr.status == 200)
                window.location.href = URLactual.origin + '/' + dir;

        }
    };
    xhr.send(formData);
}

function verMovimientoJS(mov) {

    let date = new Date(mov.fechahora);
    date.setHours(date.getHours() + 3);
    let hora = ((date.getHours() > 9) ? date.getHours() : ('0' + date.getHours())) + ':' + ((date.getMinutes() > 9) ? date.getMinutes() : ('0' + date.getMinutes())) + ':' + ((date.getSeconds() > 9) ? date.getSeconds() : ('0' + date.getSeconds()));
    let dia = date.getFullYear() + '-' + ((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '-' + ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate()));
    document.getElementById('apellido-0')['value'] = mov.apellido;
    document.getElementById('nombre-0')['value'] = mov.nombre;
    document.getElementById('observaciones-0')['value'] = mov.observaciones;
    document.getElementById('movimiento-0')['value'] = mov.tipo;
    document.getElementById('fecha-0')['value'] = dia;
    document.getElementById('hora-0')['value'] = hora;
    document.getElementById('nrosocio-0')['value'] = mov.nrosocio;
    document.getElementById('legajo-0')['value'] = mov.legajo;
    $('#modalver0').modal('show')

}
 

function editarPersonalJS(per) {

    let modal = document.getElementById('modaledita0');
    document.getElementById('nombre-0')['value'] = per.nombre;
    document.getElementById('apellido-0')['value'] = per.apellido;
    document.getElementById('codigomarcado-0')['value'] = per.codigomarcado;
    document.getElementById('entmatutina-0')['value'] = per.horaentradamat;
    document.getElementById('entsabados-0')['value'] = per.horaentradasab;
    document.getElementById('entvespertina-0')['value'] = per.horaentradaves;
    document.getElementById('salmatutina-0')['value'] = per.horasalidamat;
    document.getElementById('salsabados-0')['value'] = per.horasalidasab;
    document.getElementById('salvespertina-0')['value'] = per.horasalidaves;
    document.getElementById('huella-0')['value'] = per.huella;
    document.getElementById('nrosocio-0')['value'] = per.nrosocio;
    document.getElementById('legajo-0')['value'] = per.legajo;
    document.getElementById('id-0')['value'] = per.id;
    $('#modaledita0').modal('show')

}
function filtrarJS(n,dir){
    let URLactual = window.location;
    switch (n) {
        case "nombre": 
            window.location.href = URLactual.origin + "/" + dir +"?fil=lconcat(per_nombre,per_apellido);%"+document.getElementById('txtnombre')['value']+"%";
            break;
        case "fecha": 
            window.location.href = URLactual.origin + "/" + dir +"?fil=idate(rlm_fechahora);"+document.getElementById('txtfecha')['value']+"";
            break;
        case "tipo": 
            window.location.href = URLactual.origin + "/" + dir +"?fil=irlm_tipo;"+document.getElementById('txttipo')['value']+"";
            break;
    
        default:
            break;
    }
}
