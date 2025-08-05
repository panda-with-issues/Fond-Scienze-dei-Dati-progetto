'use strict'

const addAnchor = document.getElementById('add-anchor')
const addRow = document.getElementById('add-row')
const formRow = document.querySelector('.form-row')

addAnchor.addEventListener('click', e => {
  formRow.classList.toggle('form-row')
  addRow.classList.toggle('form-row')
})