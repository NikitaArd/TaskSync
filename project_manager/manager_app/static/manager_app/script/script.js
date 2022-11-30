function getCookie(name){
  const value = `; ${document.cookie}`;
  const clear_cookies = value.split(`; ${name}=`);
  if (clear_cookies.length === 2) return clear_cookies.pop().split(';').shift();
}

const csrf_token = getCookie('csrftoken')

$(function(){
    $('#menuToggle').on('click', function(){
        $('#menu').toggleClass('menu-open');
        $('#menuToggle').toggleClass('menuToggleRotate');
    });
})

function dialogOpener(id){
    document.getElementById(id).classList.add('dialog-active');
}

function dialogCloser(id){
    document.getElementById(id).classList.remove('dialog-active');
}

$(function(){
    $('.avatar').on('click', function(){
        Array.prototype.forEach.call($('.avatar'), function(item){
            item.classList.remove('avatars-active');
        });
        this.classList.add('avatars-active');
    })
})

$(function(){
    $('#avatar-change-submit').on('click', function(){
        change_avatar_ajax(document.getElementsByClassName('avatars-active')[0].id)
    })
})

function open_more(id) {
    section_more = document.getElementById(`card_more-${id}`);
    card_elem = document.getElementById(`card-${id}`);
    card_wrapper = card_elem.parentElement;
    Array.prototype.forEach.call($('.card-more'), function(item){
        if (item != section_more){
            item.classList.remove('projects-card-active');
        }
    });
    Array.prototype.forEach.call($('.projects-card-wrapper'), function(item){
        if (item != card_wrapper){
            item.classList.remove('projects-card-wrapper-active');
        }
    });
    section_more.classList.toggle('projects-card-active');
    card_elem.parentElement.classList.toggle('projects-card-wrapper-active');
}

$(function(){
    $('.avatar').on('click', function(){
        submit_button = document.getElementById('avatar-change-submit-href')
        avatar_id = document.getElementsByClassName('avatars-active')[0].id;

        submit_button.href = `accounts/information/change/avatar/${avatar_id}`;
    })
})

function render_user_item(user_uuid, username, avatar){
    return `<div class="dialog-project-settings-user-item">
                <span>
                    <img src="${avatar}" alt="user avatar">
                </span>
                <p id="${user_uuid}">${username}</p>
                <button id="delete-user-from-project"></button>
            </div>
    `
}

function delete_user_from_project(event){
    user_to_delete = event.target.previousElementSibling.id;
    $.ajax({
            type: 'POST',
            url: `${window.location.href}ajax/delete_user/`,
            data: {
                    user_uuid: user_to_delete,
                    csrfmiddlewaretoken: csrf_token,
            },

            success: function(response){
                    document.getElementById(user_to_delete).parentElement.remove();
            },

            error: function(response){
                    alert(response['responseJSON']['error_message']);
            },
    })
}

function add_user_to_project(event){
    user_email = document.getElementById('add-user-form-input').value
    if(user_email.length > 4){
        $.ajax({
                type: 'POST',
                url: `${window.location.href}ajax/add_user/`,
                data: {
                        user_email: user_email,
                        csrfmiddlewaretoken: csrf_token,
                },

                success: function(response){
                        document.getElementById('add-user-form').classList.toggle('dialog-project-settings-user-form');
                        $('#add-user-form').before(render_user_item(response['user_uuid'], response['username'], response['user_avatar_url']));
                },

                error: function(response){
                        alert(response['responseJSON']['error_message']);
                },
        })
    }
}

$(function(){
    $('#add-user-button').on('click', function(){
        document.getElementById('add-user-form-input').value = ''
        document.getElementById('add-user-form').classList.toggle('dialog-project-settings-user-form')
    })
})

$(function(){
    $(document).on('click', '#add-user-to-project', add_user_to_project);
});

$(function(){
    $(document).on('click', '#delete-user-from-project', delete_user_from_project);
});
