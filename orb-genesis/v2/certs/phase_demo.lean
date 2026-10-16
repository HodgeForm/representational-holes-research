set_option maxRecDepth 200000
set_option maxHeartbeats 0
inductive V | i (n : Int) | s (x : String) | b (x : Bool) deriving DecidableEq
structure Row where
  id : String
  obs : List (String × V)
  out : String
deriving DecidableEq
inductive E | field (a : String) | eq (a b : String) | xor (a b : String) | sum (a b : String) | diff (a b : String)
def get (r : Row) (f : String) : V := (r.obs.lookup f).getD (V.s "")
def truthy : V → Bool | V.i n => n != 0 | V.b x => x | V.s x => x != ""
def ev (r : Row) : E → V
  | E.field a => get r a
  | E.eq a b => V.b (decide (get r a = get r b))
  | E.xor a b => V.b (truthy (get r a) != truthy (get r b))
  | E.sum a b => match get r a, get r b with | V.i x, V.i y => V.i (x+y) | _, _ => V.s "type-error"
  | E.diff a b => match get r a, get r b with | V.i x, V.i y => V.i (x-y) | _, _ => V.s "type-error"
def key (m : List E) (r : Row) : List V := m.map (ev r)
def predict (train : List Row) (m : List E) (r : Row) : Option String :=
  match train.filter (fun t => decide (key m t = key m r)) with
  | [] => none
  | h :: rest => if rest.all (fun t => decide (t.out = h.out)) then some h.out else none

def studyHash : String := "691b4227c398bf5e8ac580190251b40d3dd129425d8acc32479d45d2798bb1fd"
def claimedStatus : String := "HELDOUT_SUPPORTED"
def train : List Row := [
  { id := "train-0", obs := [("color", V.s "dark"), ("phase", V.s "in"), ("shape", V.s "round"), ("temperature", V.i (10))], out := "stable" },
  { id := "train-1", obs := [("color", V.s "dark"), ("phase", V.s "in"), ("shape", V.s "round"), ("temperature", V.i (20))], out := "stable" },
  { id := "train-2", obs := [("color", V.s "dark"), ("phase", V.s "out"), ("shape", V.s "round"), ("temperature", V.i (10))], out := "unstable" },
  { id := "train-3", obs := [("color", V.s "dark"), ("phase", V.s "out"), ("shape", V.s "round"), ("temperature", V.i (20))], out := "unstable" },
  { id := "train-4", obs := [("color", V.s "light"), ("phase", V.s "in"), ("shape", V.s "square"), ("temperature", V.i (10))], out := "stable" },
  { id := "train-5", obs := [("color", V.s "light"), ("phase", V.s "in"), ("shape", V.s "square"), ("temperature", V.i (20))], out := "stable" },
  { id := "train-6", obs := [("color", V.s "light"), ("phase", V.s "out"), ("shape", V.s "square"), ("temperature", V.i (10))], out := "unstable" },
  { id := "train-7", obs := [("color", V.s "light"), ("phase", V.s "out"), ("shape", V.s "square"), ("temperature", V.i (20))], out := "unstable" }]
def val : List Row := [
  { id := "test-8", obs := [("color", V.s "dark"), ("phase", V.s "in"), ("shape", V.s "round"), ("temperature", V.i (30))], out := "stable" },
  { id := "test-9", obs := [("color", V.s "dark"), ("phase", V.s "in"), ("shape", V.s "round"), ("temperature", V.i (40))], out := "stable" },
  { id := "test-10", obs := [("color", V.s "dark"), ("phase", V.s "out"), ("shape", V.s "round"), ("temperature", V.i (30))], out := "unstable" },
  { id := "test-11", obs := [("color", V.s "dark"), ("phase", V.s "out"), ("shape", V.s "round"), ("temperature", V.i (40))], out := "unstable" },
  { id := "test-12", obs := [("color", V.s "light"), ("phase", V.s "in"), ("shape", V.s "square"), ("temperature", V.i (30))], out := "stable" },
  { id := "test-13", obs := [("color", V.s "light"), ("phase", V.s "in"), ("shape", V.s "square"), ("temperature", V.i (40))], out := "stable" },
  { id := "test-14", obs := [("color", V.s "light"), ("phase", V.s "out"), ("shape", V.s "square"), ("temperature", V.i (30))], out := "unstable" },
  { id := "test-15", obs := [("color", V.s "light"), ("phase", V.s "out"), ("shape", V.s "square"), ("temperature", V.i (40))], out := "unstable" }]
def lang : List E := [E.field "shape"]
def rule : List E := [E.field "shape", E.field "phase"]
def r1 : Row := { id := "train-0", obs := [("color", V.s "dark"), ("phase", V.s "in"), ("shape", V.s "round"), ("temperature", V.i (10))], out := "stable" }
def r2 : Row := { id := "train-2", obs := [("color", V.s "dark"), ("phase", V.s "out"), ("shape", V.s "round"), ("temperature", V.i (10))], out := "unstable" }
theorem r1_in : r1 ∈ train := by decide
theorem r2_in : r2 ∈ train := by decide
theorem conflict : key lang r1 = key lang r2 ∧ r1.out ≠ r2.out := by decide
theorem obstruction : ¬ ∃ f : List V → String, f (key lang r1) = r1.out ∧ f (key lang r2) = r2.out := by
  intro ⟨f, h1, h2⟩
  rw [conflict.1] at h1
  exact conflict.2 (h1.symm.trans h2)
theorem heldout_supported : val.all (fun r => decide (predict train rule r = some r.out)) = true := by decide
#print axioms obstruction
#print axioms heldout_supported
