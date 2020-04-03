## The Silverfish Programming Language

They say, each professional developer must have done at least three pet projects: a sophisticated logging utility, a smart json parser, and an amazing programming language. Once we have both logger and parser accomplished, we finally decided to reveal our desperate success in creation one of the most innovative programming languages named _Silverfish_.

![Карасик → На самом деле плотвичка](https://habrastorage.org/webt/s8/r4/lh/s8r4lhx77zsoxdk84ndas9jd0aw.jpeg)

<cut>

As we all know, the universe is constantly moving around. Evolution of programming languages is not even close to completion. New languages emerge every year to undergo the laboratory testing on human beings and die in oblivion, sooner or later. The vast majority of innovations in any new language could barely be considered as a result of new development, but as the evolution of well-known approaches or even reinvention of old good wheels.

While working on _Silverfish_ we were inspired by such successful projects as _rust_, _python_, _c++_, _wolfram_, and experimental creatures, such as _dcastf_, _glink_, _whitespace_ and many others that although have not conquered the world, but remain very valuable and enlightening.

So, welcome to our brand new majestic development language, _The Silverfish_.

### Right Assignment Syntax

Ages ago when computers were huge and dinosaurs were tiny, the founding fathers made a mistake in sewing up the assignment operator the right-to-left behavior, which is contrary to what would be intuitively expected (unless your mother language is Farsi).

This right-to-left religion left (pun is intended) its stigma on many technologies, making us to perceive:

- Assembly instruction `mov` confusing students by the order of the arguments for the seventh decade already;
- `C` standard library functions, such as `strcpy`, `memmove` etc drive students bonkers because there is neither logic nor at least some consistency in their argument order.

Still it would be fine if we have always enjoyed the right-to-left paradigm, but the thirst for naturalness spawned:

- command-line utilities `cp`, `ln`, etc.
- the syntax of the functions in the standard `C++` library, such as `std::copy` and its family.

The dichotomy of directions led to the fact that instead of unstoppably writing code, the developer is forced to pause, walk to the coffee machine for another espresso and lazily move back to the comfortable chair to review hundreds of pages of the respective documentation.

Luckily enough, after decades of industry stagnation in regard to this issue, there has been a recent shift. The vast majority of modern tools pick up left-to-right as the default direction as opposed to right-to-left. While the order of arguments in the library functions is still given away to project maintainers’ will,  assignment operators that built into the syntax of programming languages survived despite any modern tendency. There came the time to hammer a nail of the righteous wrath to the coffin of prosperous irrationality, which is called, yeah, the assignment operator.

_Silverfish_ language introduces the right (yes, _the_ right) assignment.

```
42 => answer
foo(42) => answer
```

Understanding the imperfections of human nature and the inability of the greater part of the community for such radical rebuilding, we did not banish the old assignment operator of the language completely. One can still use it, with the warning prompty spat into the developers’ face.

Optional assignment direction: left-to-right and right-to-left:

![LtR vs RtL](https://habrastorage.org/webt/8w/xb/wd/8wxbwde-dze44sfdur3fdtd9l0a.jpeg)

By the way, the syntax below is also perfectly valid and can be used for some hacks:

```
42 => answer = 42
```

### Type Management; Interpreter vs Compiler

There are unceasing debates getting into the fight, what typing is preferable, _static_, _dynamic_, _structural_, _nominative_, or _else_. _Silverfish_ rides all the horses at once, allowing the developer to change the typing from line to line.

```
<typing:dynamic> // dynamic typing :: globally on

fn foo(a, b) // this code is dynamically typed
{
    a + b => c
    return c
}

fn bar(a:i32, b) // dynamically typed, nominative type check
{   
    a + b => c
    return c
}

[typing:static] // local function annotation :: statically typed
fn fubar(a:i32,b:i32) -> i32 // this code is statically typed
{
    a + b => c : i32
    return c

    // other ways to return the value from function
    // a + b => return
    // a + b
}
```

When we introduced the changeable typing, we at some point discovered that it opens fairly wide approach to optimizations, since the static part can be compiled (the interpreter executes it in _jit_ mode for the native processing instructions.) If the whole application is configured to be fully statically typed, it’s even possible to compile it into an executable file. (Technically we can do it with dynamic code, but in this case we are to deliver the interpreter, the virtual machine and the whole jungle within the code.)

In addition to static and dynamic typing, _Silverfish_ also presents the _kinematic typing_. This is a brand new kind of typing, recently invented by the academic community. Details of this kind of typing are out of scope of this introductory article, because this topic is worthy of a three-thousand-page book. Just to give an idea, the _kinematically typed_ variable would depend on the types of all the local and global variable in the respective scope, the object tree and the Earth’s axis direction because _complete_ is a composition of _portable_ and _relative_, as stated in the Holy book:

![Statics / Dynamics / Kinematics](https://habrastorage.org/webt/gw/io/2a/gwio2a28qb88ufsq-b4xrmpgmsg.jpeg)

### Spaces vs Tabs

_Silverfish_ offers a beautiful solution to the eternal question, what should be preferred, tabs or spaces. This solution was inspired by _whitespace_ language, which roughly proofs its inviolability and rightness. We gracefully admire the idea of _Go_ authors to use `tab`-only doctrine to indicate margins and forbid any space-padding in general, but we decide that the arbitrary proclaiming _tabs_ as the truth in the last instance violates the rights of white-spaced minorities, which is contrary to modern society movement toward tolerance and diversity.

In _Silverfish_, _tabs_ and _spaces_ have different meanings!

```
    a + foo(b) => c // tabs
    a + foo(b) => c // spaces
```

These two expressions look the same, but there is a huge difference. The difference is in the exception handling. Everyone knows that code design like 

```
try {
    foo();
}
catch (...) {}
```

swallowing exceptions is quite popular among developers. We decided to let this design to penetrate into the language core syntax. Now, one can explicitly suppress exceptions by whitespace indentation. The code of Mighty Spacers would run smoothly while the code of Vile Tabbers would raise inevitably.

### Error Handling

In addition to the aforementioned graceful error handling (aka _spaces_ vs _tabs_ round,) _Silverfish_ has a genuinely elaborated system of dealing with exceptional cases.

In addition to the classical methods, such as exception handling based on archaic `try`-`catch`

```
try {
    throw Exception(42);
} catch ex {
    print(ex.value)
    exit(0)
}
```

and built-in support for unioned result

```
fn foo() -> result(i32) 
{
    return Exception(42)
}
```

_Silverfish_ has many contemporary features to handle errors, such as widely discussed in the past, but never actually implemented, `tryso` clause, which, when an exception is caught, opens the new page in the browser and automatically searches the error on _Stack Overflow_.

```
tryso {
    throw Exception(42)
}
```

We are also proud to introduce the `tryso_explicit` version that instead of performing a passive lookup at _Stack Overflow_, posts a question with a comprehensive error description. Paid versions of _Silverfish_ would immediately upvote this question from all the community accounts and push the question to IDEs of users of free version.

```
tryso_explicit {
    throw Exception(42)
}
```

There is also `force_retry` macro, that enforces the code to be re-executed until it finally runs properly.

```
force_retry {
    throw Exception(42)
}
```

![Einstein](https://habrastorage.org/webt/l5/q8/a9/l5q8a9ytavdhnshukuplp7iqzak.jpeg)

Under some circumstances, `force_retry` might not be a perfect fit; in this cases we have `smart_try` to the rescue. The latter executes the code only if it looks more or less valid.

```
smart_try {
    throw casdcasd sdfsadf Exception(42) // this would never get executed
}
```

In addition, there is a rather useful core function `shallow_throw(N)` which throws an exception that gets propagated not more than `N` levels higher on the call stack.

```
shallow_throw(n) Exception(42)
```

What would be the real use-case of the above remains unclear to the authors of the language, but they leave it as is in a hope the community would come up with something here.

### Lazy Internet Computing

The solution of many computational problems is extremely easy to find in the internet search engines. Therefore, the smart _Silverfish_ interpreter, when encounters a particularly complicated calculation, does take any action upon it directly, but rather googles it for the previously published solution. Thus, the calculation of factorials of large numbers, or Fibonacci numbers, or like this has in _Silverfish_ the complexity `O(1)`. This revolutionary method sometimes even allows _Silverfish_ to predict and produce in the runtime (or compilation time for static variants) exception in the case when the algorithm would never return.

That is, _Silverfih_ is occasionally able to solve the notorious [Halting Problem](https://en.wikipedia.org/wiki/Halting_problem).

![](https://habrastorage.org/webt/mh/mq/ky/mhmqkyr2wad6srhuhifvfcrn0fq.jpeg)

If _Silverfish_ was unable to find an acceptable solution in the internet, it indeed performs the calculation itself and publishes it back to the internet. Both poor financial resources and considerations of ethical nature prevents us from storing in our datacenters everything calculated by _Silverfish_ worldwide. Instead, _Silverfish_ takes an advantage of decentralized storage, pushing the results to random forum boards. That perfectly works thanks to the aforementioned approach to google this data when needed by another piece of the application.

### Smart Language

They say, the developer’s time is quite expensive. A considerable amount of this time is spent not on writing code and building software architecture, but on non-stop fighting with spelling errors and syntactic inaccuracies. Modern languages in general are very intolerant to human imperfection.

Not _Silverfish_ though.

![Clowns](https://habrastorage.org/webt/6v/qu/3o/6vqu3ozplarbvl46bcpvkc1rwmc.jpeg)

An explicitly designed artificial intelligence module is built into the interpreter. Once stumbled on a syntax or spelling error, it’d predict what the developer had in mind, and run the _proper_ code instead. Performance is not affected at all, especially if the interpreter is tweaked to use all these parallel computing gpu rocket science.

AI is also trained to give advices in regard to design patterns and architectural issues. It also might be configured to switch mentoring mode on so that it can take over the patronage of novice developers.

In the upcoming version of the language, the voice assistant would be included to make it possible to generate the code based on the voice commands. Tightly coupled with the suggestion lookup and existing solution search, it is designed to allow performing development for people who had never seen the computer before. The pre-release version is already able to understand voice commands like “I need an accounting system” and “Create me a site by tonight.”

### Import of Dynamic Libraries and Modules 

The maturity of architectural solutions, artificial languages and software designs, as well as the versatility of typing, allows _Silverfish_ to build generic interfaces for interoperability with other languages that do not require special bindings or wrappers, as used in `lua`, `python` and other languages. Binding external libraries is straightforward.

The import package from python, one might use

```
import python3:numpy as np

fn main() 
{
    np.arange([42,41,40]) => arr
    np.log10(arr)
}

```

To import the `C` standard library:

```
import clang:string.h as cstring
import clang:stdlib.h as cstdlib

fn main() 
{
    raw_buffer(cstdlib.malloc(40),40) => buf0
    cstring.strcpy(buf0, "HelloWorld")

    println(buf0) // HelloWorld
}
```

Rigorous readers would surely notice that this kind of import support brings the enormous capabilities of integrating all the existing languages and technologies into _Silverfish_, and it certainly does. There is no doubt that in the future there will be _alpha and omega_ programming language that will unite everything, and, winning the contest against _Disney Studio_, will connect all the Sith and Jedi at once, not by clusters.

![Brigade](https://habrastorage.org/webt/4-/s4/mo/4-s4mow04xnoxyuj6lyo4krcdt8.jpeg)

### Standard Protocols and RFC Support

_Silverfish_ comes with a set of libraries supporting all the most common standards and technologies, including but not limited to

#### RFC1149

```
fn main() 
{
    rfc1149.datagramm("HelloFriend") => dgramm
    rfc1149.send_bird("c/de Marina 16, this Friday, 7AM to 2PM", dgramm)
}
```

#### RFC2795

```
import rfc2795

fn main() 
{
    rfc2795.monkey("Jonh") => john
    rfc2795.monkey("George") => george
    rfc2795.monkey("Stephen") => stephen

    rfc2795.monkey_group([jonh, george]) => jonh_and_george

    "" => sonnet    
    do  
    {
        john_and_george.make_sonnet(66) => sonnet
    } while(stephen.do_critic(sonnet) is false)

    println(sonnet)

    /*

    Tired with all these, for restful death I cry,
    As, to behold desert a beggar born,
    And needy nothing trimm'd in jollity,
    And purest faith unhappily forsworn,
    And guilded honour shamefully misplaced,
    And maiden virtue rudely strumpeted,
    And right perfection wrongfully disgraced,
    And strength by limping sway disabled,
    And art made tongue-tied by authority,
    And folly doctor-like controlling skill,
    And simple truth miscall'd simplicity,
    And captive good attending captain ill:

    Tired with all these, from these would I be gone,
    Save that, to die, I leave my love alone. 

    */
}
```

### Conclusion

Here comes the time when we shall be proud to introduce the prototype of the language and publish the source code to the public domain. This landmark event will surely happen and then the IT world would never be the same. _Silverfish_ would not pass unnoticed to the public, for it has all the chances to become one of the most important and long-lived languages in the whole history of the industry, before to give way to new, even better languages.

_Silverfish_ re-interpreted everything in a new way, in the truly spirit of times. We believe that soon we’ll see offers for developers positions in _Silverfish_, here and there.

There would be _Silver Junior Fisher_, _Silver Middle Fisher_, and many recommendative articles on how to interview _Silver Senior Fisher_ here and there.

So let _Silverfish_ be sailing confidently toward a brighter future. Hurray, comrades!

### Acknowledgments

The author is grateful to Aleksei Matiushkin (aka chapuza) for the translation and adaptation into English.

### Copyright

© provided by Silver Fisher Inc. All rights reserved.
 
![Thanks for pay attention](https://habrastorage.org/webt/so/e0/yu/soe0yuykvtgbymwygegtzeyd7y4.png)