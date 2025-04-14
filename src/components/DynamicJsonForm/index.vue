<template>
    <div>
      <!-- 动态表单渲染 -->
      <el-form :model="formData" ref="form" label-width="150px">
        <el-form-item v-for="(value, key) in formData" :key="key" :label="key">
          <template v-if="typeof value === 'object' && !Array.isArray(value)">
            <!-- 递归渲染嵌套对象 -->
            <DynamicForm :json="value" v-model="formData[key]" />
          </template>
          <template v-else-if="Array.isArray(value)">
            <!-- 渲染数组 -->
            <div v-for="(item, index) in value" :key="index">
              <el-input v-model="value[index]" placeholder="Input value" />
            </div>
          </template>
          <template v-else-if="Array.isArray(value)">
            <div v-for="(item, index) in value" :key="index">
                <!-- 使用 v-model 绑定数组的指定元素 -->
                <el-input v-model="formData[key][index]" placeholder="Input value" />
            </div>
            </template>
        </el-form-item>
      </el-form>
  
      <!-- 提交按钮 -->
      <el-button type="primary" @click="submitForm">Submit</el-button>
    </div>
  </template>
  
  <script>
  import { ref, defineComponent } from 'vue';
  import { ElForm, ElFormItem, ElInput, ElButton } from 'element-ui';
  
  // 子组件：动态表单
  const DynamicForm = defineComponent({
    props: {
      json: {
        type: Object,
        required: true
      },
      modelValue: {
        type: Object,
        required: true
      }
    },
    setup(props) {
      return {
        formData: props.modelValue
      };
    },
    watch: {
      json: {
        handler(newJson) {
          this.formData = newJson;
        },
        deep: true
      }
    },
    // render() {
    //   return (
    //     <el-form model={this.formData} label-width="150px">
    //       {Object.keys(this.json).map(key => {
    //         const value = this.json[key];
    //         return (
    //           <el-form-item label={key} key={key}>
    //             {typeof value === 'object' && !Array.isArray(value) ? (
    //               <DynamicForm json={value} v-model={this.formData[key]} />
    //             ) : Array.isArray(value) ? (
    //               value.map((item, index) => (
    //                 <el-input v-model={this.formData[key][index]} key={index} />
    //                 ))
    //             ) : (
    //               <el-input v-model={this.formData[key]} />
    //             )}
    //           </el-form-item>
    //         );
    //       })}
    //     </el-form>
    //   );
    // }
  })
  
  export default {
    name: 'DynamicJsonForm',
    components: {
      ElForm,
      ElFormItem,
      ElInput,
      ElButton,
      DynamicForm
    },
    props: {
      json: {
        type: Object,
        required: true
      }
    },
    setup() {
      const formData = ref(JSON.parse(JSON.stringify(this.json)));
  
      const submitForm = () => {
        console.log('Submitted Data:', formData.value);
        // 可以在这里添加提交逻辑，例如通过Axios提交给后端
      };
  
      return {
        formData,
        submitForm
      };
    }
  };
  </script>
  
  <style scoped>
  .el-form {
    margin: 20px;
  }
  </style>
  