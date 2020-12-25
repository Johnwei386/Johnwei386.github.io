---
layout:     post
title:      SpringBoot源码学习(一)
subtitle:   深入研究SpringBoot源码
date:       2020-12-25
author:     Johnwei386
header-img: img/post-bg-rwd.jpg
catalog: true
tags:
    - Spring
    - SpringBoot
    - SpringFramework
---

## SpringBoot简介

SpringFramework是java企业级开发领域举足轻重的开发框架，在SpringFramework之前，J2EE是java企业级开发的主流框架解决方案，SpringFramework自诞生的第一天伊始便主要以轻量级的容器解决方案迅速赢得深受J2EE问题折磨的Java程序员的热情追捧。Spring框架的核心是IOC控制反转和AOP面向切面编程，用户通过自定义的XML文件和注解类文件，然后，Spring框架容器自动解析，导入并生成相应的类实例，使用户专注于具体的业务模块开发任务。但是，spring框架使用配置文件来生成类实例，维护类实例的方式，在遇到众多需要加载的类实例面前，造成配置地狱的问题，即大量的类的Bean和类之间的依赖关系需要用户在XML文件或注解类中写明和维护，其编写和维护的复杂度已然超出可接受的范围。

SpringBoot是Spring提出的一个用来解决配置地狱问题现行的主流Java企业级开发解决方案，它在SpringFramework的基础上，提供了一个自动加载的配置方式，避免了配置地狱问题，使开发人员可以通过SpringBoot自由的组装Spring的各个组件，得到自己想要实现的功能，生成最终的目标程序。原有的SpringMVC的开发模式早已式微，使用SpringBoot直接开发Web应用可以绕过原来开发SpringMVC项目的复杂配置环节。SpringBoot是Spring构建微服务开发体系的基础地位，如下图所示，SpringBoot提供构建微服务应用的基础架构，Spring Cloud提供连接各微服务模块的基础网络机制，SpringCloudDataFlow提供一个更加友好、优化程度更高的数据流解决方案。

![](/img/jwblog/springboot/springEcosystem.png)




