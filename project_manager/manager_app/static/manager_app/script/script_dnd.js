let draggables = document.querySelectorAll('.draggable')
let containers = document.querySelectorAll('.container')
const board = document.querySelectorAll('.manager-window-columns')

// init cookies
function getCookie(name){
  const value = `; ${document.cookie}`;
  const clear_cookies = value.split(`; ${name}=`);
  if (clear_cookies.length === 2) return clear_cookies.pop().split(';').shift();
}

const project_uuid = getCookie('p_uuid')
const user_id = getCookie('u_uuid')
const username = JSON.parse(document.getElementById('json-username').textContent)

// init sockets
const tasksUrl = `ws://${window.location.host}/ws/project/${project_uuid}/`


const tasksSocket = new WebSocket(tasksUrl)

// onmessage functions
tasksSocket.onmessage = function (e) {
  let data = JSON.parse(e.data)
  if(data['request_type'] == 'task_shift'){
    prev_item = document.getElementById(data['prev_task'])
    item = document.getElementById(data['task'])
    if(prev_item){
      prev_item.after(item);
    } else {
      $(document.getElementById(data['column']).lastElementChild.previousElementSibling).prepend(item);
    }
  }
  if(data['request_type'] == 'task_add'){
    $(document.getElementById(data['column_uuid']).lastElementChild.previousElementSibling).append(render_task(data['new_task_content'], data['new_task_uuid']));
    updateDraggalbeElements();
  }
  if(data['request_type'] == 'task_status_edit'){
    document.getElementById(data['task_uuid']).classList.toggle('task-item-done');
  }
  if(data['request_type'] == 'task_delete'){
    document.getElementById(data['task_uuid']).remove();
  }
  if(data['request_type'] == 'task_content_edit'){
    document.getElementById(data['task_uuid']).lastElementChild.previousElementSibling.innerHTML = data['new_content'];
  }
  if(data['request_type'] == 'column_add'){
    $('.column-add').before(render_column(data['column_name'], data['column_uuid']));
    window.location.reload();
  }
  if(data['request_type'] == 'column_delete'){
    document.getElementById(data['column_uuid']).remove();
  }
  if(data['request_type'] == 'column_name_edit'){
    document.getElementById(data['column_uuid']).firstElementChild.innerHTML = data['new_name'];
  }
  if(data['request_type'] == 'chat_message'){
    if(user_id == data['user_id']){
      $('#messages-container').append(render_message(content=data['message'], useraname=data['username'], own='self'));
    } else {
      $('#messages-container').append(render_message(content=data['message'], useraname=data['username'], own='other'));
    }

    if(document.getElementsByClassName('chat-window-active').length < 1) {
      document.getElementById('chat-notification').classList.add('chat-notification-active');
    }
    var messageBody = document.querySelector('#messages-container-wrapper');
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
  }
}

draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', () => {
        draggable.classList.add('dragging')
    })

    draggable.addEventListener('dragend', () => {
      if(!draggable.previousElementSibling) {
        ws_task_shift('', draggable.id, draggable.parentElement.parentElement.id);
      } else {
        ws_task_shift(draggable.previousElementSibling.id, draggable.id, draggable.parentElement.parentElement.id);
      }
      draggable.classList.remove('dragging');
    })
})

containers.forEach(container => {
    container.addEventListener('dragover', e => {
        e.preventDefault()
        const afterElement = getDragAfterElement(container, e.clientY)
        const draggable = document.querySelector('.dragging')

        if (draggable != null ) {
            if (afterElement == null) {
                container.appendChild(draggable)
            } else {
                container.insertBefore(draggable, afterElement)
            }
        }
    })
})

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')]
  
    return draggableElements.reduce((closest, child) => {
      const box = child.getBoundingClientRect()
      const offset = y - box.top - box.height / 2
      if (offset < 0 && offset > closest.offset) {
        return { offset: offset, element: child }
      } else {
        return closest
      }
    }, { offset: Number.NEGATIVE_INFINITY }).element
  }

  var amount = '';


let container = document.querySelector("#columns-window");
let left = document.querySelector("#span-left");
let right = document.querySelector("#span-right");

let idx;

left.addEventListener("dragenter", function(){
  idx = setInterval(() => container.scrollLeft -= 2, 4);
});

left.addEventListener("dragleave", function(){
  clearInterval(idx);
});

right.addEventListener("dragenter", function(){
  idx = setInterval(() => container.scrollLeft += 2, 4);
});

right.addEventListener("dragleave", function(){
  clearInterval(idx);
});

function updateDraggalbeElements() {
  draggables = document.querySelectorAll('.draggable')

  draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', () => {
        draggable.classList.add('dragging')
    })

    draggable.addEventListener('dragend', () => {
      if(!draggable.previousElementSibling) {
        ws_task_shift('', draggable.id, draggable.parentElement.parentElement.id);
      } else {
        ws_task_shift(draggable.previousElementSibling.id, draggable.id, draggable.parentElement.parentElement.id);
      }
      draggable.classList.remove('dragging')
    })
  })

  containers.forEach(container => {
    container.addEventListener('dragover', e => {
        e.preventDefault()
        const afterElement = getDragAfterElement(container, e.clientY)
        const draggable = document.querySelector('.dragging')

        if (draggable != null ) {
            if (afterElement == null) {
                container.appendChild(draggable)
            } else {
                container.insertBefore(draggable, afterElement)
            }
        }
    })
  })
}

//  websocket send views

function ws_task_add(column_uuid){

  tasksSocket.send(JSON.stringify({
    'request_type':'task_add',
    'column_uuid': column_uuid,

    'project_uuid': project_uuid,
    'user_id': user_id,
  }))
}

function ws_task_shift(prev_task_id, task_id, column_uuid){

  tasksSocket.send(JSON.stringify({
    'request_type': 'task_shift',
    'prev_task_uuid': prev_task_id,
    'task_uuid': task_id,
    'to_column_uuid': column_uuid,

    'project_uuid': project_uuid,
    'user_id': user_id,
  }))
}

function ws_task_delete(task_id, column_uuid){

  tasksSocket.send(JSON.stringify({
     'request_type': 'task_delete',
     'task_uuid': task_id,
     'column_uuid': column_uuid,

     'project_uuid': project_uuid,
     'user_id': user_id,
  }))
}

function ws_task_done_toggler(task_id, column_uuid){

  tasksSocket.send(JSON.stringify({
    'request_type': 'task_status_edit',
    'task_uuid': task_id,
    'column_uuid': column_uuid,

    'project_uuid': project_uuid,
    'user_id': user_id,
  }))
}

function ws_task_content_edit(task_id, column_uuid, newcontent){

  tasksSocket.send(JSON.stringify({
    'request_type': 'task_content_edit',
    'task_uuid': task_id,
    'column_uuid': column_uuid,
    'new_content': newcontent,
    
    'project_uuid': project_uuid,
    'user_id': user_id,
  }))
}

function ws_column_add(){

  tasksSocket.send(JSON.stringify({
    'request_type': 'column_add',
    'project_uuid': project_uuid,
    'user_id': user_id,
  }))
}

function ws_column_delete(column_uuid){

  tasksSocket.send(JSON.stringify({
    'request_type': 'column_delete',
    'column_uuid': column_uuid,

    'project_uuid': project_uuid,
    'user_id': user_id,
  }))
}

function ws_column_name_edit(column_uuid, newname){

  tasksSocket.send(JSON.stringify({
    'request_type': 'column_name_edit',
    'column_uuid': column_uuid,
    'new_name': newname,

    'project_uuid': project_uuid,
    'user_id': user_id,
  }))
}

function ws_message_send(message_text, username){

  tasksSocket.send(JSON.stringify({
    'request_type': 'chat_message',
    'message': message_text,
    'username': username,
    
    'project_uuid': project_uuid,
    'user_id': user_id,
  }))
}

function render_column(name, id) {   
  return `<div class="column" id='${id}'>
              <h2 class="column-title">${name}</h2>
              <ul class="container"></ul>
              <button class="task-item-add"></button>
          </div>`
}

function render_message(content, username, own) {
  return `<li class="${own}">
              <div>
                  <h3>${username}</h3>
                  <p>${content}</p>
              </div>
          </li>`
}

function render_task(content, id) {
  return `<li id="${id}" class="draggable task-item" draggable="true"><button class="task-done-button"></button><p>${content}</p><img class="show-more-in-task" src="/static/icons/show-more.svg"></li>`
}

$(function(){
  $('.task-item-add').on('click', function(){
    ws_task_add(this.parentElement.id);
  })
})

$(function(){
  $('.column-add').on('click', function(){
    ws_column_add();
  })
})

function local_message_sender(){
  message_text = document.getElementById('chat-message-input').value;
  document.getElementById('chat-message-input').value = '';
  if(message_text.length > 0) {
    ws_message_send(message_text, username);
  }
}

$(function(){
  $('#send-message').on('click', function(){
    local_message_sender();
  })
})

$(function(){
  $('#chat-message-input').on('keyup', function({key}){
    if(key == 'Enter'){
      local_message_sender();
    }
  })
})

$(function(){
  $('#chat-window-call').on('click', function(){
      $('#chat-window').toggleClass('chat-window-active');
      document.getElementById('chat-notification').classList.remove('chat-notification-active')
      var messageBody = document.querySelector('#messages-container-wrapper');
      messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
  })
})

$(function(){
  $('.task-done-button').on('click', function(){
    ws_task_done_toggler(this.parentElement.id, this.parentElement.parentElement.parentElement.id);
  })
})

function remove_all_select(){
  Array.prototype.forEach.call($('.task-item'), function(item){
    item.classList.remove('select-element');
  });
  Array.prototype.forEach.call($('.column'), function(item){
    item.classList.remove('select-element');
  });
}

function item_selector(event){
  if (event.target.tagName == 'P' || event.target.tagName == 'H2') {
    if (event.target.parentElement.classList.contains('select-element')) {
      document.getElementById('input-select-item').value = '';
      event.target.parentElement.classList.remove('select-element');
    } else {
      remove_all_select();
      event.target.parentElement.classList.add('select-element');
      document.getElementById('input-select-item').value = event.target.innerHTML;
    }

  }
}

$(function(){
  $(document).on('click', '.task-item', item_selector);
});

$(function(){
  $(document).on('click', '.column-title', item_selector);
})

$(function(){
  $('#delete-select-item').on('click', function(){
    select_elem = document.getElementsByClassName('select-element')[0]
    if(select_elem) {
      if (select_elem.classList.contains('task-item')) {
        ws_task_delete(select_elem.id, select_elem.parentElement.parentElement.id);
      }
      if (select_elem.classList.contains('column')) {
        ws_column_delete(select_elem.id);
      }
      remove_all_select();
      document.getElementById('input-select-item').value = '';
    }
    document.getElementById('input-select-item').value = '';
  })
})

$(function(){
  $('#confirm-select-item').on('click', function(){
    select_elem = document.getElementsByClassName('select-element')[0]
    if(select_elem) {
      if (select_elem.classList.contains('task-item')) {
        ws_task_content_edit(select_elem.id, select_elem.parentElement.parentElement.id, document.getElementById('input-select-item').value);
      }
      if (select_elem.classList.contains('column')) {
        ws_column_name_edit(select_elem.id, document.getElementById('input-select-item').value);
      }
      remove_all_select();
      document.getElementById('input-select-item').value = '';
    }
    document.getElementById('input-select-item').value = '';
  })
})

$(function(){
  $(document).on('click', '.show-more-in-task' ,function(){
    this.parentElement.classList.toggle('task-item-show-more');
  })
})
