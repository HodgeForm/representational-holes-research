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

def studyHash : String := "880ce3c951097a026dc7d75024966a381f81f416fae60582facf229934b606f1"
def claimedStatus : String := "HELDOUT_SUPPORTED"
def train : List Row := [
  { id := "train-0", obs := [("a", V.i (0)), ("b", V.i (0)), ("noise", V.i (1)), ("site", V.s "lab")], out := "off" },
  { id := "train-1", obs := [("a", V.i (0)), ("b", V.i (1)), ("noise", V.i (1)), ("site", V.s "lab")], out := "on" },
  { id := "train-2", obs := [("a", V.i (1)), ("b", V.i (0)), ("noise", V.i (1)), ("site", V.s "lab")], out := "on" },
  { id := "train-3", obs := [("a", V.i (1)), ("b", V.i (1)), ("noise", V.i (1)), ("site", V.s "lab")], out := "off" },
  { id := "train-4", obs := [("a", V.i (0)), ("b", V.i (0)), ("noise", V.i (2)), ("site", V.s "lab")], out := "off" },
  { id := "train-5", obs := [("a", V.i (0)), ("b", V.i (1)), ("noise", V.i (2)), ("site", V.s "lab")], out := "on" },
  { id := "train-6", obs := [("a", V.i (1)), ("b", V.i (0)), ("noise", V.i (2)), ("site", V.s "lab")], out := "on" },
  { id := "train-7", obs := [("a", V.i (1)), ("b", V.i (1)), ("noise", V.i (2)), ("site", V.s "lab")], out := "off" },
  { id := "train-8", obs := [("a", V.i (0)), ("b", V.i (0)), ("noise", V.i (3)), ("site", V.s "lab")], out := "off" },
  { id := "train-9", obs := [("a", V.i (0)), ("b", V.i (1)), ("noise", V.i (3)), ("site", V.s "lab")], out := "on" },
  { id := "train-10", obs := [("a", V.i (1)), ("b", V.i (0)), ("noise", V.i (3)), ("site", V.s "lab")], out := "on" },
  { id := "train-11", obs := [("a", V.i (1)), ("b", V.i (1)), ("noise", V.i (3)), ("site", V.s "lab")], out := "off" },
  { id := "train-12", obs := [("a", V.i (0)), ("b", V.i (0)), ("noise", V.i (4)), ("site", V.s "lab")], out := "off" },
  { id := "train-13", obs := [("a", V.i (0)), ("b", V.i (1)), ("noise", V.i (4)), ("site", V.s "lab")], out := "on" },
  { id := "train-14", obs := [("a", V.i (1)), ("b", V.i (0)), ("noise", V.i (4)), ("site", V.s "lab")], out := "on" },
  { id := "train-15", obs := [("a", V.i (1)), ("b", V.i (1)), ("noise", V.i (4)), ("site", V.s "lab")], out := "off" }]
def val : List Row := [
  { id := "val-16", obs := [("a", V.i (0)), ("b", V.i (0)), ("noise", V.i (11)), ("site", V.s "lab")], out := "off" },
  { id := "val-17", obs := [("a", V.i (0)), ("b", V.i (1)), ("noise", V.i (11)), ("site", V.s "lab")], out := "on" },
  { id := "val-18", obs := [("a", V.i (1)), ("b", V.i (0)), ("noise", V.i (11)), ("site", V.s "lab")], out := "on" },
  { id := "val-19", obs := [("a", V.i (1)), ("b", V.i (1)), ("noise", V.i (11)), ("site", V.s "lab")], out := "off" },
  { id := "val-20", obs := [("a", V.i (0)), ("b", V.i (0)), ("noise", V.i (12)), ("site", V.s "lab")], out := "off" },
  { id := "val-21", obs := [("a", V.i (0)), ("b", V.i (1)), ("noise", V.i (12)), ("site", V.s "lab")], out := "on" },
  { id := "val-22", obs := [("a", V.i (1)), ("b", V.i (0)), ("noise", V.i (12)), ("site", V.s "lab")], out := "on" },
  { id := "val-23", obs := [("a", V.i (1)), ("b", V.i (1)), ("noise", V.i (12)), ("site", V.s "lab")], out := "off" }]
def lang : List E := [E.field "site"]
def rule : List E := [E.field "site", E.eq "a" "b"]
def r1 : Row := { id := "train-0", obs := [("a", V.i (0)), ("b", V.i (0)), ("noise", V.i (1)), ("site", V.s "lab")], out := "off" }
def r2 : Row := { id := "train-1", obs := [("a", V.i (0)), ("b", V.i (1)), ("noise", V.i (1)), ("site", V.s "lab")], out := "on" }
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
