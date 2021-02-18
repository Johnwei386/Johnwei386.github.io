---
layout:     post
title:      ConcurrentHashMap学习笔记
subtitle:   对ConcurrentHashMap的一些学习笔记记录
date:       2021-02-10
author:     Johnwei386
header-img: img/post-bg-rwd.jpg
catalog: true
tags:
    - Java
    - HashMap
    - ConcurrentHashMap
---

## Intoduction
**ConcurrentHashMap**是java.util.concurrent包下的一个类，它实现了ConcurrentMap接口和Serializable接口，其继承关系如下图所示。它遵循Hashtable的方法约束，但有更好的并发支持。HashMap、Hashtable和ConcurrentHashMap三者之间，HashMap是线程不安全的，HashTable是线程安全，它通过synchronizing操作来保证线程安全，但强制加锁并不能保证高的并发性。

![](https://media.geeksforgeeks.org/wp-content/uploads/20200911154622/ConcurrentHashMapinJava.png)

## ConcurrentMap
**ConcurrentMap**是Map接口的扩展，它旨在提供一种架构方式来解决高吞吐量和线程安全之间的协调性问题。通过重写一些Map接口的默认实现方法，ConcurrentMap提供了一个指导方案，保证线程安全和内存一致性的原子操作的有效实现。同时，通过改写的默认方法支持来禁用空值作为key或value。其改写的默认方法如下：
> getOrDefault
> forEach
> replaceAll
> computeIfAbsent
> computeIfPresent
> compute
> merge
> putIfAbsent
> remove
> replace(key, oldValue, newValue)
> replace(key, value)

以上方法皆是原子性的方法，并且禁用空值.

## ConcurrentHashMap
**ConcurrentHashMap**是ConcurrentMap的实现类，它有Node类来存储一个哈希键值对，Node类有next属性来链接下一个Node，因此，多个Node可以构建一个链表，这个链表称为一个存储桶，HashMap的本质是一张哈希表，多个存储桶组成的数组便是这张哈希表。ConcurrentHashMap的哈希表采用了慢初始化策略，即在第一个Node插入后进行初始化，创建这张表的实例。可以通过锁定存储桶中的第一个Node来独立地锁定每个存储桶。读操作将不会被阻塞。

ConcurrentHashMap主要采用了**CAS(compare and swap 比较并交换)**来保证原子操作，它是原子操作的一种，可用于在多线程编程中实现不被打断的进行数据交换操作，从而避免多线程同时改写某一数据时由于执行顺序的不确定性和中断的不可预知性产生的数据不一致问题。 该操作通过将内存中的值与指定数据进行比较，当数值一样时将内存中的数据替换为新的值。
```c
int cas(long *addr, long old, long new)
{
    /* C语言CAS代码示例, CAS实现原子操作 */
    if (*addr != old){
        return 0;
    }
    *addr = new;
    return 1;
}
```
如以上C代码所示，CAS在使用上，通常会记录下某块内存中的旧值，通过对旧值进行一系列的操作后得到新值，然后通过CAS操作将新值与旧值进行交换。如果这块内存的值在这期间内没被修改过，则旧值会与内存中的数据相同，这时CAS操作将会成功执行 使内存中的数据变为新值。如果内存中的值在这期间内被修改过，则一般来说旧值会与内存中的数据不同，这时CAS操作将会失败，新值将不会被写入内存。在应用中CAS可以用于实现无锁数据结构，一般有无锁队列和无锁栈。

参数concurrencyLevel是ConcurrentHashMap独有的参数，其目的是提供一个同时访问该哈希表的预先估计的线程数，因为在Java8之前，并发段(存储桶?)的数量是与访问表的线程数相关的，以此来保证对每个并发段(存储桶?)的更新操作，一次不会超过一个线程。但从Java 8开始，提供带有concurrencyLevel参数的构造函数只是为了向后兼容，而且，concurrencyLevel参数也只能影响Map的初始大小。

## ABA问题
ABA问题是无锁结构实现中常见的一种问题，可基本描述为：
> 1. 进程P1读取了一个数值A
> 2. P1被挂起(因为时间片耗尽、中断等原因)，进程P2开始执行
> 3. P2修改数值A为数值B，然后又修改回A
> 4. P1被唤醒，比较后发现数值A没有变化，程序继续执行

对于P1来说，数值A未发生过改变，但实际上A已经被变化过了，继续使用可能会出现问题。在CAS操作中，由于比较的多是指针，这个[问题](https://zh.wikipedia.org/wiki/比较并交换)将变得更加严重。

## CAS实现
CAS操作基于CPU提供的原子操作指令实现。对于Intel X86处理器，可通过在汇编指令前增加LOCK前缀来锁定系统总线，使系统总线在汇编指令执行时无法访问相应的内存地址。而各个编译器根据这个特点实现了各自的原子操作函数。
> C语言，C11的头文件<stdatomic.h>。由GNU提供了对应的_sync系列函数完成原子操作.
>  C++11，STL提供了atomic系列函数.
>  JAVA，sun.misc.Unsafe提供了compareAndSwap系列函数。

