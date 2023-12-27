<template>
  <div class="grid grid-cols-3 gap-4 mb-4">
    <div class="rounded-t-lg bg-gray-50 h-64 dark:bg-gray-800 p-0 col-span-2">
      H1
    </div>
    <div class="rounded-t-lg bg-gray-50 h-64 dark:bg-gray-800 p-0">
      H1
    </div>
    <div class="rounded-t-lg bg-gray-50 h-64 dark:bg-gray-800 p-0">
      H1
    </div>
    <div class="rounded-t-lg bg-gray-50 h-64 dark:bg-gray-800 p-0">
      H1
    </div>
    <div class="rounded-t-lg bg-gray-50 h-64 dark:bg-gray-800 p-0">
      H1
    </div>
  </div>
</template>
<script>
import { EntryConfig } from '../../wailsjs/go/backend/App';

function CallEntryConfig() {
  EntryConfig().then((res) => {
    console.log(res)
  })
}
EntryConfig()

export default {
  name: 'HomeView',
  created() {
    
  }
}


</script>