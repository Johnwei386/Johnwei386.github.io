---
layout:     post
title:      SpringBoot源码学习(二)
subtitle:   深入研究SpringBoot源码_SpringBoot一些注解研究
date:       2021-02-03
author:     Johnwei386
header-img: img/post-bg-rwd.jpg
catalog: true
tags:
    - Spring
    - SpringBoot
    - SpringFramework
---

## @SpringBootTest
**@SpringBootTest**注解告诉SpringBoot去寻找主配置类（通常是由@SpringBootApplication注解标注的类），然后使用这个配置类开启一个Spring应用的上下文，之后可以运行所有基于SpringBoot环境的测试类。

## @EnableCaching
**@EnableCaching**注解使能Spring注解驱动的缓存管理能力，自Spring框架3.1版本开始加入到Spring Framework中，这样便不需要在xml文件写缓存管理相关的bean定义，它触发一个后端处理---扫描所有用缓存注解标注的public方法的bean。**@EnableCaching**类似于一个开关，它激活Spring缓存功能，Spring缓存适用于这样一种场景：当某个方法被多次调用时，其返回值其实可以缓存起来，当多次调用同一方法时，直接从缓存里面返回返回值即可，这样就可以节省掉多次调用同一方法的性能开销。

Spring缓存是Spring框架提供的抽象接口，框架本身不提供任何具体实现，真正的实现由第三方类库提供，一般包括以下几种实现方式：
> 1. java.util.concurrent.ConcurrentMap
> 2. EhCache
> 3. Gemfire Cache
> 4. Guava Caches
> 5. JSR 107 complaint caches

*ConcurrentMap*将会把数据缓存在内存中。Spring缓存有几个重要的注解类：@Cacheable、@CacheEvict、@CachePut、@Cahcing、@CahceConfig。@Cacheable声明一个方法是可缓存的，并给定缓存的名称。@CahceConfig声明一个缓存配置类，配置类中的所有方法都是可缓存的方法。

## @EnableScheduling
**@EnableScheduling**使能SpringBoot作业可以定期执行的功能，它是提供这样一种功能，例如可以让你每隔10秒钟运行一次作业。这需要用到@EnableScheduling和@Scheduled这两个注解，通过以下几个步骤：
#### 1. 添加@EnableScheduling注解到SpringBootApplication类
**@EnableScheduling**是一个Spring上下文模块注解，它的内部通过`@Import(SchedulingConfiguration.class)`来导入SchedulingConfiguration配置，该配置将创建ScheduledAnnotationBeanPostProcessor，它扫描被@Scheduled注解声明的beans。
#### 2. 添加@Scheduled注解在方法上
现在可以添加@Scheduled注解到你想执行定时任务的方法上了，执行该任务的方法不能含有任何参数，这是唯一的限制。

#### 示例代码
以固定时间间隔执行一个作业：
```java
@Scheduled(initialDelay = 1000, fixedRate = 10000)
public void run() {
    logger.info("Current time is :: " + Calendar.getInstance().getTime());
}
```

## @RestControllerAdvice
**@RestControllerAdvice**是SpringFramework4.3的一个新特性，它等于@ControllerAdvice + @ResponseBody，它能通过@ExceptionHandler处理RestfulApi的异常。示例代码如下：
```java
@RestControllerAdvice
public class WebRestControllerAdvice {
    @ExceptionHandler(CustomNotFoundException.class)
    public ResponseMsg handleNotFoundException(CustomNotFoundException ex) {
        ResponseMsg responseMsg = new ResponseMsg(ex.getMessage());
        return responseMsg; 
    }
}
```
`handleNotFoundException`方法将处理所有从@RequestMapping(示例代码如下)反馈的CustomNotFoundException。
```java
@RequestMapping(value="/customer/{name}")
public Customer findCustomerByName(@PathVariable("name")String name){
    Customer cust = customerService.findCustomerByName(name);
    if(null == cust){
        throw new CustomNotFoundException("Not found customer with name is " + name);
    }
    return cust;
}
```
提供了一种在Web应用环境下处理异常的机制，通过@ExceptionHandler监听设置的异常类，设置一个异常处理的方法，一般是通过getMessage方法得到该异常类的异常信息，然后返回这个异常信息，@ResponseBody将这个异常信息封装成json，然后返回给前端访问用户。

## @Component
所有被标注**@Component**注解的类将被容器在路径扫描时注册为容器中的一个bean，@Service,  @Repository,  @Controller都是特殊的@Component,

## @Service
**@Service**是@Component注解的一种特殊形式，@Service只适用于类，用于将类标记为服务提供者，Spring上下文环境将自动加载这些类。@ComponentScan确保所有被 @Component标注的类将被扫描并注册到容器中成为一个bean。

## @PostConstruct
当我们使用依赖注入配置Spring Beans时，有时我们希望在我们配置的bean开始服务客户端请求之前，一切都已经被正确的初始化，同样，当Spring上下文被破坏时，我们可以关闭被bean使用的一些资源。

这里我们使用**@PostConstruct**进行初始化操作，它是一个方法注解，一个类只能有一个方法标注@PostConstruct注解，@PostConstruct注解是`javax.annotation-api`通用注解的一部分，如果是使用java9以及更高版本的JDK时，需要引入`javax.annotation`包。

## @PreDestroy
与@PostConstruct相反，当Spring Bean实例被销毁并被移除出容器时，**@PreDestroy**注解标注的方法将执行一些资源的释放工作。总之，@PostConstruct和@PreDestroy类似于Spring Bean的构造函数和析构函数。

