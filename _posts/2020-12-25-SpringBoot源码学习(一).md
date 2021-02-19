---
layout:     post
title:      SpringBoot源码学习(一)
subtitle:   深入研究SpringBoot源码_SpringBoot自启动研究
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

以下所有SpringBoot源代码研究全部基于SpringBoot 2.4.1和SpringFramework 5.3.2

## @SpringBootApplication
**@SpringBootApplication**是SpringBoot的一个应用入口级注解，它是一个类和接口级别的注解，标示了该类是一个SpringBoot应用，一个SpringBoot应用程序只有一个用@SpringBootApplication注解的主类，@SpringBootApplication注解是@SpringBootConfiguration、@EnableAutoConfiguration和@ComponentScan这三个注解的集合体，并引用了@Inherited注解，这样所有继承自由@SpringBootApplication注解标注的类的子类会自动继承父类的注解，即@SpringBootApplication注解

@SpringBootApplication中的proxyBeanMethods属性指示是否对容器中的Bean开启CGLIB代理，CGLIB动态代理是Spring框架使用的用来实现AOP动态织入代码到class字节码中的技术实现方案。SpringBoot的所有注解最终能影响到实际的java类实例，其核心便是通过JVM虚拟机在执行代码时通过动态代理的方式(如CGLIB方法)织入注解代码到实例的class字节码文件中，实现AOP面向切面编程的重要编程思想。

proxyBeanMethods属性是自SpringBoot 2.2后增加的一个新属性，默认值为true，它使得开发人员在开发过程中，容器中的bean可以一直是同一个实例，也可以每次都生成新的实例。若设置为true，则打开CGLIB动态代理bean的生成，容器中任意时刻只有一个bean实例，这也是解决组件依赖问题的一个解决方案。

## @SpringBootConfiguration
**@SpringBootConfiguration**提供了一个SprintBoot版本的Configuration注解，它自己就包含有@Configuration注解，可以作为是@Configuration注解的替换版本。所有Spring应用应该只包含有一个@SpringBootConfiguration注解，然后大部分惯用的SpringBoot程序和该程序下的其他类将从@SpringBootApplication注解继承@SpringBootConfiguration注解。
```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Configuration
public @interface SpringBootConfiguration {
    @AliasFor(annotation = Configuration.class)
	boolean proxyBeanMethods() default true;
}
```

## @EnableAutoConfiguration
**@EnableAutoConfiguration**开启了Spring应用上下文的自动配置功能，它基于用户设置的*classpath*和已经用户定义好的bean配置进行自动配置，自动配置的过程自动计算依赖关系并将依赖的包或类等载入容器。用户可以通过设置@EnableAutoConfiguration的exclude和excludeName属性排除掉不进行自动配置的类。@EnableAutoConfiguration一般通过@SpringBootApplication注解来实现引用，不单独用来标注类，或者将其放在根包(应用根目录)，这样所有的子包和所有的类都可以被搜索到。

符合自动配置机制的类一般是带有Spring的@Configuration注解的类，可以通过**SpringFactoriesLoader**机制定位寻找。通常，自动配置的beans是@Conditional、@ConditionalOnClass和@ConditionalOnMissingBean这三种beans。

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@AutoConfigurationPackage
@Import(AutoConfigurationImportSelector.class)
public @interface EnableAutoConfiguration {
	String ENABLED_OVERRIDE_PROPERTY = "spring.boot.enableautoconfiguration";
	Class<?>[] exclude() default {};
	String[] excludeName() default {};

}
```

## @AutoConfigurationPackage
自动配置包注解，将主应用程序所在包的文件载入容器。通过`@Import(AutoConfigurationPackages.Registrar.class)`载入它的basePackages和basePackageClasses属性所包含的类到容器中。Registrar是AutoConfigurationPackages类的一个静态内部类成员，Registrar通过调用AutoConfigurationPackages类的register方法将@AutoConfigurationPackages注解的*basePackages*和*basePackageClasses*下的组件类名称传给BeanDefinitionRegistry，BeanDefinitionRegistry是用来注册和访问所有bean实例的接口，每个bean实例由BeanDefinition描述。

AutoConfigurationPackages类下有一个静态内部类PackageImports，它封装了SpringBoot自动导包的具体实现，下面的代码便是PackageImports的核心，它有一个私有属性packageNames，用来保存需要导入到容器中的所有包名称，然后在构造方法里，初始化生成packageNames，如何生成呢？它先去查找AutoConfigurationPackage的basePackages和basePackageClasses属性指定的包，如果这两个属性为空，则说明没有用户自定义的初始化导包目录，则用*packageNames.add(ClassUtils.getPackageName(metadata.getClassName()));*导入当前类所在的包到容器中，如此就实现了自动导入本开发项目所在的包中的类和资源到容器中。
```java
private final List<String> packageNames;

PackageImports(AnnotationMetadata metadata) {
			AnnotationAttributes attributes = AnnotationAttributes
.fromMap(metadata.getAnnotationAttributes(AutoConfigurationPackage.class.getName(), false));
			List<String> packageNames = new ArrayList<>(Arrays.asList(attributes.getStringArray("basePackages")));
			for (Class<?> basePackageClass : attributes.getClassArray("basePackageClasses")) {
				packageNames.add(basePackageClass.getPackage().getName());
			}
			if (packageNames.isEmpty()) {
				packageNames.add(ClassUtils.getPackageName(metadata.getClassName()));
			}
			this.packageNames = Collections.unmodifiableList(packageNames);
}
```

## @Import
**@Import**导入组件类到容器，导入的类通常是@Configuration注解标注的类，它等价于Spring XML配置文件规范中的`<import/>`标记，它可以导入带有@Configuration注解的类和*ImportSelector*和*ImportBeanDefinitionRegistrar*的实现类。在@Configuration注解类下声明的@Bean部件通过@Autowired注解实现自动装入，Spring通过@Autowired注解实现Bean的依赖注入。

@import注解的使用类似于`@Import(AutoConfigurationPackages.Registrar.class)`，这是在@AutoConfigurationPackages注解源码中的例子，@import载入AutoConfigurationPackages.Registrar配置类。


## @AliasFor注解
**@AliasFor**是一个别名注解，只作用于方法，是一个方法级的注解，其属性有三：value、attribute和annotation。如下源码所示，在AliasFor注解代码中，value和attribute通过分别引用AliasFor注解声明各自的别名，这说明AliasFor是可以自引用的一个注解接口。
```java
@AliasFor("attribute")
	String value() default "";
	
	@AliasFor("value")
	String attribute() default "";
```

AliasFor注解的作用有二：①声明别名，②指定方法的作用范围(即方法或属性所属的注解)。以@SpringBootApplication为例，其源码的一部分如下所示，scanBasePackages方法的返回值正是ComponentScan注解的basePackages属性的值，该属性指定自动加载机制扫描包中所有组件的基础包位置(如com.snail.arxiv等)，这里的AliasFor中的annotation属性指定所修饰方法所属的注解，attribute属性指定该注解的某个属性，这个属性的值正是AliasFor所修饰方法的返回值。
```java
@AliasFor(annotation = EnableAutoConfiguration.class)
	String[] excludeName() default {};
	
@AliasFor(annotation = ComponentScan.class, attribute = "basePackages")
	String[] scanBasePackages() default {};
```

## SpringBoot 自动配置研究
在@EnableAutoConfiguration引入AutoConfigurationImportSelector到容器中，AutoConfigurationImportSelector类在selectImports方法中调用getAutoConfigurationEntry方法实现自动配置，它通过调用getCandidateConfigurations方法得到需要载入容器并进行自动配置的类清单。getCandidateConfigurations方法中通过SpringFactoriesLoader类中的loadFactoryNames方法得到清单，loadFactoryNames方法则调用loadSpringFactories方法得到清单。

在loadSpringFactories方法中，调用类加载器的getResources()方法，传入参数"META-INF/spring.factories"，"META-INF/spring.factories"即要获取的资源名称，getResources将先去父类加载器寻找资源，与双亲委托模式相似，父类一般为平台类加载器，子类即当前的类加载器为应用类加载器。

寻找资源的顺序为，先去类加载器已加载的模块中去寻找资源，然后去类路径下去寻找资源，如在类路径中包含在当前项目下的*target/classes*路径，它指示当在编译java项目时需要依赖模块的支持时，类加载器去该目录下寻找已经编译好的模块。

在匹配寻找所有的类路径之后，返回一个包含有资源的类路径URL类，然后如下代码所示解析资源，得到载入和进行自动配置的类清单，在SpringBoot项目中只有在spring-boot包和spring-boot-autoconfigure包的META-INF目录下包含有spring.factories文件。
```java
Enumeration<URL> urls = classLoader.getResources(FACTORIES_RESOURCE_LOCATION);
while (urls.hasMoreElements()) {
    URL url = urls.nextElement();
	UrlResource resource = new UrlResource(url);
	Properties properties = PropertiesLoaderUtils.loadProperties(resource);
	for (Map.Entry<?, ?> entry : properties.entrySet()) {
		String factoryTypeName = ((String) entry.getKey()).trim();
		String[] factoryImplementationNames =
					 StringUtils.commaDelimitedListToStringArray((String) entry.getValue());
		for (String factoryImplementationName : factoryImplementationNames) {
			result.computeIfAbsent(factoryTypeName, key -> new ArrayList<>())
						.add(factoryImplementationName.trim());
		}
	}
}
```

**@ComponentScan**配置组件扫描，与Configuration类一起使用，提供和Spring XML元素相同的支持。它有两个属性: basePackageClasses和basePackages(或对应的别名value)指定特定的包去扫描组件。**若未设置这些属性，即未声明需要扫描的包，则去声明此注解的类所在的包扫描组件**。