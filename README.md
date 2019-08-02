## 描述 ##
主要用 middleware 实现对接 opentracing

###注意事项###
*  通过headers 来传记录ID
*  baseview.py 中 self.opentracing_header 可以获取到记录ID
*  code 主要用于记录code , 并不一定跑得通

