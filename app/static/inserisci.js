'use strict'

const mercatoInput = document.querySelector('select[name="mercato"]')
const giornoInput = document.querySelector('select[name="giorno_mercato"]')
const defaultChildren = Array.from(giornoInput.children)
const confirmationArticle = document.querySelector('.confirmation')

if (confirmationArticle) {
  setTimeout(() => {
    confirmationArticle.classList.add('confirmation-active')
    const descendants = confirmationArticle.querySelectorAll('*')
    for (const el of descendants) {
      if (el.classList.contains('hidden')) {
        el.classList.add('visible')
      }
    }
  }, 100);
}

mercatoInput.addEventListener('change', sort_giorni)
mercatoInput.addEventListener('change', removeBlank, {once: true})

if (session?.mercato) {
  mercatoInput.dispatchEvent(new Event('change'))
  mercatoInput.firstChild.selected = false
  for (const opt of giornoInput.children) {
    if (opt.value === session.giorno_mercato) {
      opt.selected = true
    }
  };
}

function sort_giorni (e) {
  defaultChildren.forEach(opt => {
    opt.selected = false
  })
  giornoInput.replaceChildren(...defaultChildren)

  const mercato = e.target.value

  const giorni = [ 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica' ]
  const idxs = []
  mercati.forEach(m => {
    if (m.mercato === mercato) {
      idxs.push(giorni.indexOf(m.giorno))
    }
  })
  idxs.sort()

  const top = []
  const children = [...defaultChildren]
  idxs.forEach((idx, i) => {
    const removed = children.splice(idx-i, 1)[0]
    top.push(removed)
  })

  const hr = document.createElement("hr")
  
  giornoInput.replaceChildren(...top, hr, ...children)
  giornoInput.firstChild.selected = true
}

function removeBlank (e) {
  Array.from(e.target.children).forEach(child => {
    if (child.value === '') {
      e.target.removeChild(child)
    }
  })
}