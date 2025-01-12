import re

# String original com os horários
text = """today we're going to talk about the branch and bound method this is a well-known and popular method
0:06
for discrete optimization it can be a kind of a general purpose method although
0:12
it's more effective for certain classes of problems we'll talk about that today but for general problems it's
0:20
not necessarily very efficient if there's other structure in the problem there are often better methods but for
0:27
certain types of problems as we'll see this is a very effective strategy
0:32
um so uh at the heart of the method we'll see one of the things that we do is sort of
0:39
this bound we're going to keep track of what a lower bound is or in other words the best solution uh
0:45
or the best the solution could possibly be and to to know that we actually have the
0:52
bound means that we have to be able to guarantee that we can solve each sub-problem and find the global
0:58
optimum there's only certain types of problems that we can guarantee that we'll find the global optimum
1:04
these are called convex problems we haven't really discussed this although we have discussed certain types of convex problems we
1:09
talked about quadratic programming problems those form the heart of the sqp where
1:16
say for example if there's equality constraints that reduce even to a linear system but for inequality we could also
1:22
guarantee convergence as long as know that quadratic term was uh positive definite
1:28
perhaps the most popular uh convex form for for these uh branch and bound problems
Linear Programming
1:34
is a linear problem so a linear problem looks like this this is just a general form
1:40
we could say let's minimize uh some coefficient of vectors times x
1:47
so c is just a vector of numbers right so these would just be some weights
1:53
and so that's a linear objective right because this would be like c1 x1 plus c2 x2 plus c3 x3 and so on
2:01
so you can see that's just linear in the variable x and all our constraints must also be
2:08
linear so we could have for example ax plus b equals 0 some equality
2:16
constraints for example we could also have and just to use a
2:21
different symbol put a hat here ax plus b-hat is less than or equal to zero for inequality
2:27
constraints so b here is a vector a is a matrix so each row of this is just a linear
2:34
constraint right it would be something like say a 1 1 x 1 plus a 1 2 x 2
2:41
plus a 1 3 x 3 plus dot dot dot plus b 1 equals 0 for example and we can
2:48
see there's just another linear equation and now we put in matrix form because there's a bunch of them
2:53
okay so this here um
2:58
we call it an lp or a linear programming problem this is convex meaning we are guaranteed
3:04
to be able to find the global optimum we can solve these very efficiently and they're very popular and say
3:10
operations research like um transportation problems networking problems uh all sorts of cases like this
3:18
uh we did we did an in-class exercise just to to recap one example where
3:23
um you actually did this in excel and that is using a branch and bound method um often
3:30
when you solve these uh linear problems with a with discrete
3:35
variables they'll use a branch and bound method but um in that example
3:41
say this was like a serious cost right we're trying to minimize some cost and so
3:46
these were the products we were making and we're making some integer number of them we're just summing up the cost and these linear constraints would be things like
3:54
resources each widget i make takes a certain amount of resources and i can't exceed some you
4:01
know specified number of resources so those are often linear constraints i want to figure out like the right mix
4:07
of products to manufacture so these kind of problems occur a lot like in
4:12
in sort of a manufacturing sense or in a transportation sense or maybe i want to minimize the distance or the cost of uh
4:19
transportation we talked about kind of this um traveling salesman like problem or say i wanted to do a a
4:25
uh this airport problem right where i was trying to go from airport to airport find a minimum cost maybe i have
4:31
um you know various constraints on on on my shipping uh that i can pose in a linear form
4:38
maybe there's some different uh weights or things that i can carry and i can't exceed a certain capacity
4:44
so these occur quite frequently in in what what is called operations research
4:49
um we can use them for other problems but we'll kind of recap that at the end they just in general are less effective because
4:56
one of the things that we're going to rely on is that we can solve a sub problem
5:02
or in other words a sub problem is going to be this problem we ignore for the moment the discrete part of it
5:09
we need to make sure that we can guarantee a solution and then it's a global optimum and that's just not possible for general problems
5:16
but we can here for these linear programming problems so this isn't really our complete problem that in itself was the lp
5:23
but then we're going to add this additional constraint and i'm just going to uh i guess i can write it this way this
5:29
is the mathematic notation here for all or some of i
5:38
this just means this is this z said this is a set of integers and the positive means it's a positive
5:44
integer so this means that all of my x's must be integers this is that integer constraint
5:50
and here we're restricting to be positive integers that's the most common case here right where we're talking about how many goods to
5:56
produce or um you know what uh nodes to connect or whatever
6:02
uh it doesn't make sense to produce a negative amount of of some good generally um although it could in that case we
6:10
could just without any loss of generality just put a negative weight here so this is actually completely general so i
6:16
guess you can ignore what i said about negatives that's that's totally acceptable here um
6:23
yeah and just to be clear that negative is captured here in the weight not not here so this is general that we assume
6:28
that these x's are positive okay so these are positive integers and so without this it's an easy problem
6:34
it's an lp but now that we've added this constraint that some of these variables um are
6:41
discrete they're integers then it becomes a bit harder and we would call this a safe works most
6:47
commonly um a mixed integer linear programming problem so this is a mi
6:53
lp mixed integer mixed meaning there's potentially some integer some continuous
6:59
variables okay so before we jump into the algorithm
Converting to Binary
7:04
one step that's very helpful is uh to convert to binary if possible
7:14
so we just said the general problem is that these x's these design variables could be integer
7:20
variables like one two three four five but it is much easier to solve usually the branch and bound
7:26
problems if our variables are binary zero or one it is often though not
7:33
always it's often possible to convert an integer problem into an equivalent binary problem sometimes we have to add
7:39
maybe additional variables or constraints or whatever but we can often do that conversion so here's an example that you can think of
7:46
so let's say we talked about some examples of integer problems actually mentioned this as discrete like i wanted to choose
7:52
the material for my car you know should i make this out titanium aluminum steel or whatever different alloys of
7:58
steel i could have a bunch of them so here's orig let's say this is my original problem i've got one design variable
8:06
and this is uh we'll i'll give it a y so it's different from the x's and y
8:12
can be 1 2 all the way up to n and these are
8:18
represent n different materials okay so that would be the way we could
8:24
specify the problem right we just map each material to a number one is steel two is aluminum and
8:30
so on and the optimizer needs to choose that design variable that fits this form
8:35
fine but to be more efficient we would like it to be a binary problem so uh you might pause at this moment
8:43
pause the video and try that see if you can convert to a binary problem
8:48
so here's something we could do to convert right so let's do some conversion here
8:55
we could say well let's make more design variables instead of having one design variable we're going to have n design
9:02
variables okay and each of these variables we want them to be binary so it's either zero or
9:08
one and so zero means don't select that material
9:16
boy have a hard time writing don't select
9:21
and one means we do select so now i have n design variables not one but n one for
9:27
every material and so it's either going to be a zero or a one i either select that material or don't
9:33
obviously that's not good enough because i need to select just one material at the end so we're also going to add a constraint
9:41
what kind of constraint could i add well i just need the sum of these to be equal to one right because i
9:47
i need everything to be zero except for one material the one that i choose so i had the constraint that
9:54
the sum of these is equal to one and that's a linear constraint so this all that's saying is that
9:59
we only can select one material so we're able to successfully convert this problem this energy problem into a
10:04
binary problem all my decision variables are now zeros or ones there are more of them and i added a
10:10
constraint so it seems like it's harder but it's actually much easier usually if we do this even
10:15
though it's a bigger problem it still ends up being easier to solve okay so we'll now go with the assumption
10:21
that we've done that let's just look at an example here one that we're going to look throughout today
10:27
here's just an example linear problem notice it has those binary constraints
10:34
so here's the objective you can see it's a linear function in x and these are all linear constraints
10:40
there's two constraints and then we have this binary constraint every x and here we don't have any
10:45
continuous variables although we could in general but each one of them has to be a zero or one
10:50
okay so um the key to solving these kind of problems or any branch and bound problem is we
10:58
use what's called a relaxation and relaxation means we're going to solve an approximate problem
11:04
where we're going to generally relax some of the constraints mean we're going to remove some of the constraints so
11:11
the first way we're going to do this and this is how we'll do it throughout this is the natural way for at least these integer problems for other more
11:17
general problems there might be other relaxations that could be better but in this case an easy relaxation is
11:23
just to say let's get rid of this all right let's get rid of that constraint then it's an easy
11:29
problem to solve uh every optimization package has linear programming solvers it's
11:35
convex right so it's guaranteed itself global optimum very efficient very fast uh it's an easy problem to solve
11:43
so that's great we can solve this problem so um and let's say
11:49
just by chance when we solve this we happen to get all zeros and ones for the answers for x
11:56
well then we'd be done right we solved the problem because we let it do whatever and it gave us theirs in one so we know that's actually
12:02
is a solution is the solution to our original problem but that's unlikely to happen right so
12:07
we have to uh keep moving forward however what it does tell us when we solve the problem it's
12:16
not it's not a solution to the problem but every time we relax it we know that we couldn't do better than
12:21
that that's a lower bound it's not a lower bound to solution yet but it's a lower bound
12:27
meaning that's the best we could possibly do because if we add these constraints back in if i
12:33
erase this it could give me the same answer if it did i would have been done already but in general adding more constraints
12:40
is means i'm going to get a worse solution right worse in the sense of the objective not worse in the sense of our
12:46
goal but a a a bigger objective what i'm trying to minimize so i know
12:54
that uh that relaxed problem is a lower bound i can't i can't do better than that okay
Branching
13:02
so that's going to be an important point that we'll use uh here's maybe a visualization of a
13:09
start on the idea of the branching portion of this so the branching portion is
13:14
we first this is this first node here is this problem where we or we got rid of this so ignore that for
13:20
the moment if we ignore that for the moment and we try and solve it and it didn't solve so now we're going to branch we're going
13:27
to try two different options because x1 only has let's say we branch
13:32
on x1 first x1 only has two options really it's only a zero or one in fact this problem is small enough
13:38
right that we could try all the combinations but of course that is not scalable as we've seen but
13:43
now i'm going to solve a new problem here where i choose x1 is 0 in this branch so this node here says
13:49
let's try let's go back to this problem here let's solve it but we'll just keep x1 0. we won't
13:55
optimize x1 we'll fix it at 0. solve for the other variables okay uh
14:02
and we could keep going right we could go down further and we could say okay now let's keep x 1 0 and x 2 0 and try to solve
14:09
for the other variables and maybe it gives me a solution maybe it doesn't uh and i could try keep going through
14:14
all of these and you'll notice right if i i did all of these branches i would have done exhaustive search
14:19
in other words i tried every combination and that's not good right because that kind of defeats the whole purpose of having an
14:26
algorithm but what we'll see is that we can eliminate branches what's going to happen
14:31
is that um uh you know we may meet some criteria say here that says we know nothing below here can be a solution
14:38
so we can just get rid of this whole thing and not evaluate it or maybe we get here and we realize okay can't go any further here we can
14:44
get rid of all of this this is called pruning when we cut off some of these branches
14:50
okay so we've kind of had two key words here so far the branch part and we've mentioned briefly the bound
14:56
part is the lower bound we're going to kind of put these together now so let's see how we could prune here's
Pruning
15:02
the diagram and this is really the key to this is that branching through every possibility is
15:08
exhaustive search but if we can prune we can cut off branches we can severely restrict the number of
15:14
combinations we have to find and still guarantee that we can find the optimum right if we have a linear
15:20
problem this is one of the cases where we can find the solution right even though we didn't try every combination
15:27
we're taking advantage of that convex structure all right so here are some some possible outcomes
15:36
let's say i solve this problem that problem where i relax the problem right so in other words
15:42
i got rid of the integer constraints and and that's going to repeat throughout right so i'm going to go through here and let's say i fixed
15:47
x1 to be 0. i still eliminate those integer constraints and i try to solve it again and let's say when i try to solve it
15:54
it's infeasible if that problem is infeasible what does
16:01
that say about the rest of that branches if i went down further
16:06
what it says is that that entire branch is infeasible
16:12
so we can prune it because if i go down further in that tree
16:17
remember all we're doing is we're adding more constraints so we're saying first just fix x1 to be 0. now fix x2 to be 0
16:24
right don't let it have anymore don't let it vary to whatever so if the problem could not be solved
16:29
before fixing one of those variables and not letting it move is not going to let it be solved and easier right now it's it's still
16:35
infeasible so once i find any solution that's infeasible let's let's say
16:42
this one here is infeasible that means all of these are also infeasible and so i don't have to evaluate them right so
16:50
in other words the general the general principle is if i can solve a problem like i and and really for this
16:56
to work i have to guarantee that i have actually know that it's infeasible and this works in this case convex if i know for sure
17:02
it's infeasible then adding more constraints can never change that right that won't ever make it any more feasible
17:10
okay so we could prune that's great so another is that let's say the objective
17:18
[Music] is worse
17:23
than our best solution
17:30
if the objective is worse than the best solution then what does it say about points that are further down on the
17:36
branch remember every time we go down the branch we're adding more and more constraints
17:42
well if we add more constraints and again this is true if we can make sure we're getting the global optimum adding more constraints will
17:48
never improve the objective it might it may not make it worse but it can't make it better
17:53
so we know that if we found a solution that's already not better than the best we found then nothing from that point on will be
17:58
better so we could prune that as well so let's say we got to this point here we say oh this is
18:04
we have a solution and here this isn't a solution even it may not even be a solution it's just it's the relaxed problem but
18:12
we we know it's already not better than the best so adding more constraints even if there are solutions down there
18:17
we know that they're worse than the best we've found so we can get rid of all of these and not evaluate that
18:22
branch so if the objective is worse and the best solution we can prune and i guess the obvious
18:30
implication there is that we do need to keep track of what our best solution is so we can compare
Solution
18:36
okay so those are those are the two pruning parts the two other possibilities is that we
18:41
find a solution okay so maybe we find a solution and
18:46
that means you know we get to some point here let's say i get to here and even though i didn't constrain
18:52
everything you know i constrain x1 and x2 and x3 and x4 and whatever other variables happen to give me integers
18:59
then that's a solution right i i satisfied that constraint of the binary zeros and ones so that's done
19:07
so that's or the problem is not done because there may be many solutions here right enough to find the best but that means i can prune
19:16
right in other words i save that solution i compare it to the best but there's no need going further right
19:21
because again adding more constraints can't improve it so even if there were and there really can't be but if there
19:27
are other solutions on that branch they can't be better so
19:32
uh that's it right so this is a lot of things i can do to prune here
19:38
otherwise we have to keep going that's really the fourth possibility is that we don't have a solution
19:45
but it still looks promising it could be better than the best it's still feasible so we have to keep
19:50
branching and go further down on that tree all right
19:59
so again this is the point and i'll come back to this again
20:04
these kind of points especially these two um actually really even the third is
20:10
what hinges on the fact that we can find the global optimum for this relaxed problem this is why
20:15
we need something like an lp a linear program problem or other convex problems because those we can guarantee
20:21
it it's a general problem um and we're pruning because we say well it can't get any better
20:26
that might be because it can't get better it might be just because we found a local optimum and you know we prune too early so
20:32
we're not necessarily going to find the best solution it's uh and each of these sub problems becomes
20:38
more complicated right because we have to solve a sequence of them so anyway we'll get back to that later this
20:43
is the method let's kind of go through an example now well actually for example i'm going to talk about a few um sort of design choices here on
20:52
the method so one question is um which variable to
20:57
branch on so above figures i just branched on
21:03
x1 first and then x2 just you know just for a picture but um let's say i solve a problem
21:11
and there's only four variables and this is my relaxed problem i get uh just make something up here let's say i got one
21:18
point two point six zero point one or whatever okay
21:25
um two of these are already integers so i don't need to branch on them they might change later right they're
21:31
still free to change uh but these ones i i should branch on because they're fractional
21:37
so i'm going to take a branch i could do any one of these but a very a common choice is to branch
21:43
on the one that is closest to 0.5 meaning it it's you know not close to zero or one the
21:50
logic there is that these ones that are maybe closer to zero or closer to one they would say well they're they're
21:55
maybe getting there right that probably could nudge that way more easily and
22:01
here we're forcing a decision faster we're saying okay let's just force it try it with a zero try it with a one and
22:06
resolve it so it tends to be more efficient if we if we use that component that's lar biggest fractional
22:14
component i mean it's closest to 0.5 another design choice is should we do a
22:20
depth first or a breadth breadth first
22:27
okay that means when we branch should i continue down this branch all the way to the bottom until i can't go any further
22:32
and then work my way up or should i go here and then here and then here and then here and here and here
22:38
and you know back up as i need of course but what's the strategy and most commonly uh depth first is
22:45
usually desirable and the reason is that by forcing more and more and more constraints we usually force a solution faster and
22:52
that's helpful because once we have a solution we can compare it to others and that helps us prune faster
22:57
usually it also means we don't need as much of a history because when we're doing depth first
23:03
we just only have to keep track based on the number of nodes but if we do breadth first we have to the amount of things we have
23:10
to keep track of and to keep in memory to compare grows as we get further and further down
23:17
anyway so most commonly depth first although in examples today i'll actually show breadth first just
23:22
because it's easier to show with these small examples and actually i think in the one case it went faster so
23:28
i just uh we'll we'll do that today all right so here's that same problem we're looking at
Example
23:34
so let's step through an example here uh and work it um i actually won't solve all the sub
23:39
problems but you can do that this example is in the book i'm just going to show you kind of the steps so what was the first
23:45
step again first step was to relax the problem
23:50
and i guess i was maybe being not specific enough i said we're going to eliminate these constraints which is
23:56
true but we're not going to just eliminate them we're going to replace them with bound constraints so we're going to say
24:02
we're making it a continuous problem but we are going to say that they should stay between zero and one right it makes no sense for
24:09
us to just allow it to be whatever right it could give us two fifty whatever because we know at the end it either has to be a zero or one
24:16
so let's keep it within those bounds at least it's still a continuous problem it's still a linear constraint easy to
24:21
solve it's even a bound constraint so we can solve this still really easily so let's say we do
24:28
that okay we solve it um and here's what we get here's the solution that linear problem and again you could plug this into any
24:34
linear programming solver it'll be easy for the optimizer to deal with this
24:41
and so we get 1 0.5 i'm just going to write two decimal
24:46
places here to from brevity 0.53 zero point uh
24:52
two decimal places that's five zero one okay so those are my variables um
25:00
and the optimal f just for interest here is minus 5.03 just with two decimal
25:06
places so this is not a solution right because i have two that are binary but these two are not so i have
25:14
to branch i'm going to branch on the one that's closest to 0.5 which is this one on x3 okay so what does that mean so here's
25:21
again here's that first solution we saw i'm branching on x3 so i'm going to solve this same problem
25:28
the same problem except for i'm going to now take x3 out of it i'm going to say in this step let's just
25:33
say x3 equals zero so it's not a design variable anymore and now i can i can let x1
25:39
x2 and x4 very freely right still within these bounds but they can vary freely
25:45
okay and that's going to be this node the other node is same problem but force x3 to be one so
25:52
x3 is forced to be one and then we let the others go freely okay
25:57
so here's what happens here right x3 was forced to be zero and we let the other three vary freely
26:04
and in this case uh it's still not a solution so we're going to continue and let's try this side right normally i
26:10
said we do depth first but you know for this picture it's actually easier for me to show you breath first so here let's do this breath one and here
26:17
we solve the problem remember we fixed x3 to be one we let the others vary notice right all the others are free to
26:23
vary so even though x4 was one before it's not one now we didn't force it to be one right we're letting it be
26:29
whatever it wants to be um and it's uh this is also not a
26:34
solution so we have to keep going okay notice that each time we there's
26:39
another thing notice each time we go down right this constraint or sorry this objective this is our lowest bound this is the best that could
26:45
possibly occur now we know it's not a solution so the real solution is going to have a higher objective
26:51
so as i go down and i've added more constraints notice each of these is worse they could be the same but they can't be better okay so now
26:59
this is i know i can't do better than that at least on this branch here so let's let's keep going
27:06
here actually this was pretty close right one zero one so the only one i could branch on is
27:11
this x2 so let's branch on that okay so here we are i branched on x2
27:18
and so so now i still force x3 is forced to be zero and x2 is forced to be zero and i let
27:24
one and four go free i let them be whatever within the bounds zero and one and they both hit the
27:30
bounds that was the best solution could find with those constraints so this is a solution that's great so
27:35
we're going to keep track of that we're now saying the best this is the best solution we've found so something we're going to compare to
27:43
f star is minus 4. it doesn't mean there are another solution we don't know that we've actually solved it we just know
27:48
that anything any number that is um already bigger than that
27:58
well we know that this is a lower bound we can't anything that's a solution or sorry any
28:04
any value that's higher than that is not going to be useful
28:10
okay so let's keep going um
28:17
i'm just going to say something on that i don't know i'm not sure i said that right let me get back to that in a sec here so let's do this next i'll recap that
28:24
here at the end so let me just finish the rest of this row here okay so i solved the next one because
28:30
again i still have this branch i wasn't able to prune it yet uh here it is right so we fixed x3 at
28:36
zero we fixed x2 at one let the other two vary uh we get a solution it's not a solution
28:41
right because this is still not binary so we would in general have to continue
28:47
here this one gave us a solution this is uh all binary values so this is a solution
28:53
and this is now our new best minus 4.9 is the best and then this one is not a solution
28:59
but here's the thing that we notice is that now we have updated our best it's minus 4.9
29:04
so anything that is worse than that um
29:12
yeah i know what i misspoke on let me correct that in a second um anything that is worse than that uh
29:26
yeah sorry i'm thinking of two things at once okay so anything anyway this is a solution so this this means that this
29:31
value here we know as we go further we're adding more constraints so this objective
29:36
cannot improve further right anything that's below here is going to be bigger than minus 4.49 but we already
29:44
know that we have a solution that's minus 4.9 so there is no need to continue this branch
29:49
any further right anything below there is either going to be minus 4.49 or worse right bigger same with this
29:57
branch here right we got minus 4.52 so there's nothing uh you know if we keep
30:03
going we could branch further but we know even if there's a solution there it's not going to be better than this one
30:08
right because minus 4.52 is already worse um yeah
30:16
so okay yeah i i i did speak correctly right so the idea here is that this was minus four let's say that this value
30:23
here was um minus three it was already a worse solution we wouldn't even have
30:29
had to evaluate those but because it's minus five it's not a solution but we know that there might be a solution that's still
30:35
really good right because this is giving us minus five but as we come down and now we got new value minus four point nine anything that's bigger than
30:42
that which is this and this we can prune so now we're done we've pruned every branch there's nowhere else to go
30:48
so this is the answer this is the optimum the only solution to this or
30:55
yeah not the only solution i guess the solution this is the global optimum to our discrete problem
31:00
and we're able to do that again because of this linear structure that we're taking advantage of that we know we can solve those sub problems globally
31:07
okay so again an important point to note here is that even though there was a solution we're not done we have to make sure we've exhausted uh
31:14
each or pruned every branch and again this is not an exhaustive search here because we only went two
31:19
levels x3 and x2 there could have been two more and of course in general there could be
31:24
lots right depending on the variables so that was breadth first i'm not going to walk through it entirely but i just
31:30
want to show you what it looks like with depth first in this case so uh here the the depth first was just
31:35
always to go left first so we branched on x3 like before um that was not a solution so we branched
31:41
again we found this solution exactly like we did before so then we come back up we come here it's not a solution so we branch
31:48
we found a new solution but it's worse it's worse than this one right so keep going branched
31:55
another solution it's still not as good branch and then this is infeasible we've now constrained everything and it's
32:00
actually not a solution so we back all the way up come down and here we get a solution this is a our
32:07
new best minus 4.9 so we save it and then we come here and it's bounded just like it is
32:13
here right this is it gives us minus 4.49 so we know well that's worse than the best we've
32:19
found so far so there's no need to continue in this case the breadth first happened to be faster just because the solution
32:24
was here but in general depth first is usually a preferred strategy
32:30
okay so what if you couldn't use binary we talked about this whole thing with binary and as we said you can often
32:37
convert integer problems to binary but if you couldn't another thing you can do is you could do
32:43
the same kind of idea so let's say we're required to have integers right um and uh let's say um you know i've got 1
32:53
3 6.27 let's say these are my variables and i now want to branch on this one
32:58
i can't make it 0 and 1 but i could do this i could say let's do one branch where x3 has to be less
33:05
than or equal to 6 and then the other where x3 has to be greater than or equal to 7.
33:10
so we're trying to put those integers on those bounds and because it wanted to be in between those two it's likely that it's going to hit
33:16
one of those bounds not necessarily though this tends to well this is in general
33:23
not as efficient i'll just show you as a picture i'm not going to walk through in real detail but this is in the book
33:29
here's another problem another linear problem you can see and here this one is mixed so
33:34
the first three variables one two and three have to be integers not binary just any integer and x4 is continuous just
33:41
any continuous variable you know positive variable
33:46
so here's uh what this looks like so we branch for example on x3 and based on what its value was we said
33:53
it had to be less than equal to four greater than equal to five and then we keep doing that um
33:58
you'll see though that uh one of the problems of this method is that in the binary case as you branch you
34:04
would never visit a variable more than once because every variable only has one possibility or two possibilities right it's either
34:10
zero or one so once we branched on x3 you would never see x3 appear again in another branch but here it does right so
34:17
x3 is less than equal to four but then we also see well maybe x3 is less than or equal to two we're tightening those constraints
34:23
um x3 is greater than equal three right so uh just because we added one constraint
34:29
we may have to add other constraints to kind of tighten that window and so these branches can become quite a bit longer
34:35
sometimes whereas they're bounded for the the binary case that's one reason why we uh the binary is advantageous
34:44
okay so as a final point here just to recap we did everything in the context of
34:49
linear or really convex problems in general but you can do this for a general
34:54
problem and uh there are branch and bound methods for that we basically use a similar type of idea
35:00
where we use these kind of constraints we'll take these continuous constraints and try to
35:05
branch on constraints the problem in that case is that this is not a guaranteed method it's just a
35:12
heuristic that we hope it will work well uh but because we're not guaranteed to find the global optimus step
35:18
a lot of those uh pruning steps can be overly optimistic and and you know not
35:24
give us a good solution the sub problems because we solve a whole bunch of problems if they're not
35:30
convex and easily solvable that can become uh expensive you know especially because these trees can be large for large for
35:37
large numbers of variables so if you don't have a linear problem it's usually only practical with a
35:42
smaller number of variables otherwise the you know the tree it gets too complicated but anyway
35:47
uh that's branch and bound this is like i said this is a popular method so if you are solving a mixed integer linear
35:53
program it's likely that the algorithm you're using is a branch and bound inbound it's like i said
35:58
particularly effective for these linear problems or or other convex problems
36:04
okay so uh next time we'll continue our discussion with discrete optimization see you uh see then"""

# Expressão regular para encontrar padrões de horários no formato "minuto:segundo"
pattern = r'\b\d{1,2}:\d{2}\b'

# Remover os horários usando re.sub
cleaned_text = re.sub(pattern, '', text)

# Remover espaços extras ou quebras de linha duplicadas
cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

print(cleaned_text)


