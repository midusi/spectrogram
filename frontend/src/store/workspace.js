import { writable } from 'svelte/store'
import apiWorkspace from '../api/workspace'
import { spectrogramStore } from './index'
import {
  loadingAlert, errorAlert, closeAlert, showAlert
} from '../helpers/Alert'

function createStoreWorkspace() {
  const { subscribe, update } = writable({
    state: {
      loading: true,
      error: false
    },
    paths: [],
    imageProperties: {}
  })

  return {
    subscribe,
    getPaths: async (dirPath) => {
      loadingAlert()
      try {
        const response = await apiWorkspace.allPaths({
          path_dir: dirPath
        })
        update((prev) => {
          prev.paths = response.data.paths
          return prev
        })
        closeAlert()
      } catch (error) {
        update((prev) => {
          prev.state.error = error
          return prev
        })
        errorAlert({ message: error.response.data.message })
      }
      update((prev) => {
        prev.state.loading = false
        return prev
      })
    },
    getImg: async (spectrogramCanvas, dirPath, imgName) => {
      loadingAlert()
      try {
        spectrogramCanvas.deleteAllBbox()
        spectrogramStore.getPredictions(
          spectrogramCanvas,
          dirPath,
          imgName
        )
        const response = await apiWorkspace.getImg({
          dir_path: dirPath,
          img_name: imgName
        })
        const { data } = response

        spectrogramCanvas.loadImage(`data:image/png;base64,${data.image}`, data.info.width, data.info.heigth)

        update((prev) => {
          prev.imageProperties = data.info
          return prev
        })
        closeAlert()
      } catch (error) {
        update((prev) => {
          prev.state.error = error
          return prev
        })
        errorAlert()
      }
      update((prev) => {
        prev.state.loading = false
        return prev
      })
    },
    saveConfig: async (config) => {
      loadingAlert()
      try {
        await apiWorkspace.saveConfig({
          config
        })
        showAlert({ title: 'Configuración Guardada', message: 'Se guardo la configuración exitosamente.' })
      } catch (error) {
        errorAlert()
      }
    },
    loadConfig: async () => {
      try {
        const response = await apiWorkspace.loadConfig()
        if (response.data !== {}) return response.data.config
      } catch (error) {
        errorAlert()
      }
      return {}
    }
  }
}

export const workspaceStore = createStoreWorkspace()