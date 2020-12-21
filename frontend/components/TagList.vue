<template>
  <div class="flex items-center flex-wrap mb-6">
    
    <div 
    @click="$emit('setSelectedTag', tag.name)"
    class="flex items-center cursor-pointer rounded-lg px-2 mr-1 mt-1 text-lg font-normal" 
    :class="tag.name === selectedTag ? 'bg-green-300 hover:bg-green-300' : 'bg-gray-300 hover:bg-gray-400' "
    v-for="tag in uniqueTags">
      <div>        
      {{ tag.name }} 
      </div>
      <div class="rounded-full bg-gray-100 text-xs px-1 ml-1">
      {{ tag.count }}        
      </div>
    </div>
    
  </div>
</template>

<script>
export default {
  name: "TagList",
  data() {
    return {
      uniqueTags:[
        { name:'all', count: this.projectData.length }
      ],
    };
  },
  props: {
    projectData: Array,
    selectedTag: String,
  },
  created() {

    this.projectData.filter((project)=>{
        return project.tags.filter((tag)=>{
          if(this.uniqueTags.some(t => t.name.toLowerCase() === tag.toLowerCase())) {
            this.uniqueTags.find((o)=>{
              if(o.name.toLowerCase() === tag.toLowerCase()){
                return o.count+=1
              }
            })
          } else {
            this.uniqueTags.push({ name: tag, count: 1 })
          }
        })
    })
    
    // this.projectData.sort(()=> {
    //   return Math.random() - 0.5
    // })
    
    // TODO Move this duplicate sorting block inside ProjectList.created()
    this.projectData.sort((a,b)=> {
        return a.twitter_followers_count < b.twitter_followers_count ? 1 : (a.twitter_followers_count > b.twitter_followers_count ? -1 : 0)
    })
    
    this.uniqueTags.sort((a,b) => {
      return a.count < b.count ? 1 : (a.count > b.count ? -1 : 
      a.name > b.name ? 1 : (a.name < b.name ? -1 : 0)
      )
    })
    
    
  }
}
</script>